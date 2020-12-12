from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,Permission, _user_get_permissions
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField('username', max_length=50, null=True, unique=True)
    score = models.IntegerField('score', default=0)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username


class Token(models.Model):

    user = models.OneToOneField(User, verbose_name='user', on_delete=models.CASCADE)
    token = models.TextField('token')