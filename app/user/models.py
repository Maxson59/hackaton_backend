from django.db import models  # noqa
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
import os
import uuid


def user_image_file_path(instance, filename):
    """ Generate file path for user profile image. """

    extension = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{extension}'

    return os.path.join('uploads', 'user', filename)


class UserManager(BaseUserManager):
    """ Manager for users. """

    def create_user(self, email, password=None, **extra_fields):
        """ Create, save and return a new user. """

        if not email:
            raise ValueError('User must have an email address.')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Create, save and return a new superuser. """

        superuser = self.create_user(email, password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system. """

    email = models.EmailField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    primer_apellido = models.CharField(max_length=255)
    imagen = models.ImageField(null=True, upload_to=user_image_file_path)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()
