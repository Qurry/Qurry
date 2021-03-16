import secrets
import uuid
from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from media.models import Image

from users.validators import HPIEmailValidator, validate_word_characters

from .managers import UserManager


def clean_email_address(email_address):
    return email_address.lower().replace('uni-potsdam.', '')


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(
        'email address', unique=True, validators=[HPIEmailValidator()])
    username = models.CharField(
        'username', max_length=50, null=True, unique=True, validators=[
            MinLengthValidator(limit_value=3),
            validate_word_characters
        ])

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def full_clean(self, *args, **kwargs):
        if self.email:
            self.email = clean_email_address(self.email)
        if self.is_blocked():
            raise PermissionError(
                'this user is blocked. please contact the support')

        super(User, self).full_clean(*args, **kwargs)

    def is_blocked(self):
        return BlockedUser.objects.filter(email__iexact=self.email)

    def block(self):
        BlockedUser.objects.create(email=self.email)
        self.delete()

    def get_profile(self):
        try:
            return self.profile
        except:
            return self.create_default_profile()

    def score(self):
        return self.get_profile().score

    def add_to_score(self, number):
        self.get_profile().score += number
        self.get_profile().save()

    def profile_image(self):
        return self.get_profile().image_url()

    def profile_info(self):
        return {**self.as_detailed(), **{
            'email': self.email,
            'registeredAt': str(timezone.localtime(self.registered_at).replace(microsecond=0))
        }}

    def as_preview(self):
        return {
            'id': str(self.id),
            'username': self.username
        }

    def as_detailed(self):
        return {**self.as_preview(), **{
            'score': max(self.score(), 0),
            'image': self.profile_image(),
        }}

    def is_owner_of(self, obj):
        return obj.user == self

    def create_default_profile(self):
        return Profile.objects.create(user=self)


class BlockedUser(models.Model):
    email = models.EmailField('email address', unique=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Profile',
                                on_delete=models.CASCADE)

    score = models.IntegerField('Score', default=0)
    image = models.ForeignKey(Image, verbose_name='Profile Image',
                              blank=True, null=True, on_delete=models.SET_NULL)

    def image_url(self):
        if self.image:
            return self.image.src.url
        return ''

    def __str__(self):
        return str(self.user)


class Token(models.Model):

    user = models.OneToOneField(User, verbose_name='user',
                                on_delete=models.CASCADE)
    value = models.TextField('token value', blank=True)
    created_at = models.DateTimeField('Creation Date', auto_now_add=True)

    token_length = 30
    expiration_time = 60

    class Meta:
        abstract = True

    def new_for(self, user):
        self.__class__.objects.filter(user=user).delete()

        self.user = user
        self.value = secrets.token_urlsafe(self.token_length)
        self.save()
        return self

    def is_valid(self):
        now = datetime.now(timezone.utc)
        return (now - self.created_at).seconds < self.expiration_time


class ActivationToken(Token):
    expiration_time = settings.ACTIVATION_TOKEN_VALIDITY_TIME


class ResetToken(Token):
    validation = models.TextField('validation token', blank=True)

    expiration_time = settings.REST_TOKEN_VALIDITY_TIME

    def new_for(self, user):
        self.validation = secrets.token_urlsafe(self.token_length)
        return super().new_for(user)
