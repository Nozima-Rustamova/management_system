from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    '''manager for custom user model'''

    def create_user(self, email, password=None, **extra_fields):
        '''create   and return a regular user'''
        if not email:
            raise ValueError("User must have an exmail adress")

        email=self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        '''create and return a superuser'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    '''custom user model that supports email instead of username'''

    email=models.EmailField(max_length=255, unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    is_teacher=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)

    objects=UserManager()

    USERNAME_FIELD='email'

    def __str__(self):
        return self.email


