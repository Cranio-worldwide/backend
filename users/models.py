import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from api.utils import translate_field, transliterate_field

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Base class for user registration,
    email is used instead of username.
    """
    DOCTOR = 'doctor'
    CUSTOMER = 'customer'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (DOCTOR, 'Doctor'),
        (CUSTOMER, 'Customer'),
        (ADMIN, 'Admin')
    )
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(
        'user role',
        max_length=50,
        choices=ROLE_CHOICES,
        default=DOCTOR
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Specialist(CustomUser):
    """
    Class for creating a user: Specialists.
    """
    first_name = models.CharField(
        blank=True, max_length=150, verbose_name='first name'
    )
    last_name = models.CharField(
        blank=True, max_length=150, verbose_name='last name'
    )
    photo = models.ImageField(
        null=True,
        blank=True,
        upload_to='media/%Y-%m-%d'
    )
    about = models.TextField(blank=True)
    phone = models.CharField(max_length=17, unique=True)
    beginning_of_the_experience = models.PositiveSmallIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1923),
                    MaxValueValidator(datetime.date.today().year)])
    diploma_issuer = models.CharField(max_length=255, blank=True)
    diploma_recipient = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, **kwargs):
        self.first_name_en, self.first_name_ru = transliterate_field(
            self.first_name_en, self.first_name_ru)
        self.last_name_en, self.last_name_ru = transliterate_field(
            self.last_name_en, self.last_name_ru)
        self.about_en, self.about_ru = translate_field(
            self.about_en, self.about_ru)
        super(Specialist, self).save()
