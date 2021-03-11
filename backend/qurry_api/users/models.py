import secrets
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from media.models import Image

from .managers import UserManager


def clean_email_address(email_address):
    return email_address.lower().replace('uni-potsdam.', '')


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField('email address', unique=True)
    username = models.CharField(
        'username', max_length=50, null=True, unique=True)

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
        super(User, self).full_clean(*args, **kwargs)

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
            'registeredAt': str(timezone.localtime(self.registered_at))
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


class ActivationToken(models.Model):
    user = models.OneToOneField(User, verbose_name='user',
                                on_delete=models.CASCADE)
    token = models.TextField('token', blank=True)

    def save(self, *args, **kwargs):
        self.token = secrets.token_urlsafe(30)
        return super().save(*args, **kwargs)

    def token_for(user):
        return ActivationToken.objects.create(user=user).token

    def is_token_valid_for(user, token):
        try:
            ActivationToken.objects.get(user=user.id, token=token).delete()
        except ActivationToken.DoesNotExist:
            return False
        return True
