from django.contrib.auth.models import AbstractUser
from django.db import models


class DoctorUser(AbstractUser):
    """Doctor model class."""

    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True
    )

    def __str__(self):
        return self.first_name
