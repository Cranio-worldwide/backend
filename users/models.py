from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет Юзера с заданным email и паролем.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        """
        Создает и сохраняет суперпользователя с заданным email и паролем.
        """

        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    """
    Базовый класс для регистрации пользователей,
    вместо username используется email.
    """
    email = models.EmailField(
        'адрес электронной почты',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
