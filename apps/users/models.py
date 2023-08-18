import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.services.translations import (
    translate_field, transliterate_field,
)

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the specified email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the specified email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Base class for user registration, email is used instead of username.
    """
    class Role(models.TextChoices):
        SPECIALIST = 'SPECIALIST', 'Specialist'
        CUSTOMER = 'CUSTOMER', 'Customer'
        ADMIN = 'ADMIN', 'Admin'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(
        verbose_name='user role',
        max_length=50,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    first_name = models.CharField(
        verbose_name='First name', blank=True, max_length=50
    )
    middle_name = models.CharField(
        verbose_name='Middle name', blank=True, max_length=50
    )
    last_name = models.CharField(
        verbose_name='Last name', blank=True, max_length=50
    )
    photo = models.ImageField(
        verbose_name="Photo",
        null=True,
        blank=True,
        upload_to='photo/%Y-%m-%d',
    )
    phone = models.CharField(
        verbose_name='Phone number',
        max_length=17,
        unique=True,
        blank=True,
        null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def save(self, **kwargs):
        """Translate blank transliterate first & last name."""
        self.first_name_en, self.first_name_ru = transliterate_field(
            self.first_name_en, self.first_name_ru)
        self.middle_name_en, self.middle_name_ru = transliterate_field(
            self.middle_name_en, self.middle_name_ru)
        self.last_name_en, self.last_name_ru = transliterate_field(
            self.last_name_en, self.last_name_ru)
        super(CustomUser, self).save()
