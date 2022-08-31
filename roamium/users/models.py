from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
    PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):

    def _check_fields(self, fields):
        for field_name, value in zip(self.model.REQUIRED_FIELDS, fields):
            if not value:
                raise ValueError(f'The {field_name} value must be set')

    def create_user(
        self, email, first_name, last_name, password=None, **kwargs
    ):
        '''Creates a user with email and password'''
        if not email:
            raise ValueError('The email value must be set')
        self._check_fields((first_name, last_name))
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **kwargs
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, **kwargs
    ):
        '''Creates an admin with email and password'''
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom User model that supports using email instead of username'''
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
