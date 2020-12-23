import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, _user_get_permissions
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager
from media.models import Image


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField('email address', unique=True)
    username = models.CharField(
        'username', max_length=50, null=True, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def as_preview(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def is_owner_of(self, obj):
        return obj.user == self


class Token(models.Model):

    user = models.OneToOneField(
        User, verbose_name='user', on_delete=models.CASCADE)
    token = models.TextField('token')


class Profile(models.Model):

    user = models.OneToOneField(
        User, verbose_name='User', on_delete=models.CASCADE)
    score = models.IntegerField('Score', default=0)
    image = models.ForeignKey(Image, verbose_name='Profile Image',
                              blank=True, null=True, on_delete=models.SET_NULL)
