from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email=None, username=None, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, username=None, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **kwargs)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)  
    role = models.CharField(
        max_length=10, choices=(('ops', 'Ops'), ('client', 'Client')), default='client'
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
