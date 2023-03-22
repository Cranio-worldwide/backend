from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Базовый класс для регистрации пользователей,
    вместо username используется email.
    """
    DOCTOR = 'doctor'
    CUSTOMER = 'customer'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (DOCTOR, 'Доктор'),
        (CUSTOMER, 'Пользователь'),
        (ADMIN, 'Администратор')
    )
    email = models.EmailField('email address', unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(
        'роль пользователя',
        max_length=50,
        choices=ROLE_CHOICES,
        default=DOCTOR
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class DoctorUser(CustomUser):
    """
    Класс для создания пользователя: Терапевт.
    """
    first_name = models.CharField(
        blank=True, max_length=150, verbose_name='first name'
    )
    last_name = models.CharField(
        blank=True, max_length=150, verbose_name='last name'
    )
    photo = models.ImageField(null=True, blank=True, upload_to='avatars/')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=50)
    office = models.CharField(max_length=50)
    about = models.TextField(blank=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    # почему валюта ФК и на что? Может сделать на первое время выпадающий
    # список из 2-5 валют?
    # currency =

    # для поля телефона есть сторонняя библиотека PhoneNumberField
    phone = models.CharField(max_length=17, unique=True)
    experience = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True
    )
    diploma = models.CharField(max_length=50, blank=True)
    # поля ниже надо обсудить
    # loc_latitude =
    # loc_longitude =
    # role =
    # active =
