from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


class User(AbstractUser, PermissionsMixin):
    username = None

    email = models.EmailField(max_length=150, verbose_name='электронная почта', unique=True)
    password = models.CharField(max_length=100, verbose_name='пароль')
    phone = models.CharField(max_length=50, unique=True, verbose_name='номер телефона', null=True, blank=True)
    avatar = models.ImageField(upload_to='user', null=True, blank=True, verbose_name='аватар')
    name = models.CharField(max_length=100, verbose_name='имя')
    surname = models.CharField(max_length=100, verbose_name='фамилия')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
