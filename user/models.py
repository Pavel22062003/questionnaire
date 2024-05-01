from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True, max_length=255)
    phone = models.CharField(max_length=35, verbose_name='телефон', null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
