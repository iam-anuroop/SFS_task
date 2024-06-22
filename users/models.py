from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

class User(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name='email address')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    user_type = models.CharField(
        max_length=10, choices=(('ops', 'Operations'), ('client', 'Client')), default='client'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
