from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)
from django.utils.crypto import get_random_string

from utils.model_mixins import BaseAppModelMixin


class SMEAPIUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser, BaseAppModelMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.TextField(blank=True, null=True)

    objects = SMEAPIUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.


class Profile(BaseAppModelMixin):
    """extend the User model with more custom property"""
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')


class ApiKey(BaseAppModelMixin):
    """extend the User model with more custom property"""
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='api_key')
    key = models.CharField(unique=True, max_length=255)

    def create_key(self):
        """create a new hash key"""
        self.key = get_random_string(length=19)
        self.save()
