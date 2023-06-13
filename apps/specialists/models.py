from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.core.services.translations import (translate_field,
                                             transliterate_field)
from apps.users.models import CustomUser

from .managers import SpecialistManager
from .validators import validate_year


class Specialist(CustomUser):
    """
    Class for creating a user: Specialists.
    """
    role = CustomUser.Role.SPECIALIST
    objects = SpecialistManager()

    class Meta:
        proxy = True

    def __str__(self):
        return self.email

    @property
    def data(self):
        return self.specialistdata


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'SPECIALIST':
        SpecialistData.objects.create(user=instance)


class SpecialistData(models.Model):
    class Status(models.TextChoices):
        FILLING = 'FILLING', _('application should be filled in')
        DIPLOMA_CONFIRMATION = 'CHECKING', _('pending diploma confirmation')
        CORRECTION_REQUIRED = 'CORRECTING', _('application should be amended')
        PENDING_PAYMENT = 'PAYMENT', _('pending payment')
        ACTIVE = 'ACTIVE', _('active therapist')

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(
        verbose_name='first name', blank=True, max_length=150
    )
    last_name = models.CharField(
        verbose_name='last name', blank=True, max_length=150
    )
    photo = models.ImageField(
        verbose_name='specialist photo',
        null=True,
        blank=True,
        upload_to='photo/%Y-%m-%d',
    )
    about = models.TextField(
        verbose_name='about specialist', blank=True)
    phone = models.CharField(
        verbose_name='phone number',
        max_length=17,
        unique=True,
        blank=True,
        null=True
    )
    practice_start = models.PositiveSmallIntegerField(
        verbose_name='year of practice start',
        blank=True,
        null=True,
        validators=[validate_year],
    )
    diploma_issuer = models.CharField(
        verbose_name='organization-issuer of diploma',
        max_length=255,
        blank=True
    )
    diploma_recipient = models.CharField(
        verbose_name='name of diploma recipient mentioned in diploma',
        max_length=100,
        blank=True,
    )
    status = models.CharField(
        verbose_name='status of specialist',
        max_length=50,
        choices=Status.choices,
        default=Status.FILLING,
    )

    class Meta:
        verbose_name = 'Specialist'
        verbose_name_plural = 'Specialists'

    def save(self, **kwargs):
        self.first_name_en, self.first_name_ru = transliterate_field(
            self.first_name_en, self.first_name_ru)
        self.last_name_en, self.last_name_ru = transliterate_field(
            self.last_name_en, self.last_name_ru)
        self.about_en, self.about_ru = translate_field(
            self.about_en, self.about_ru)
        super(SpecialistData, self).save()

    def __str__(self):
        return f'{self.user}: {self.first_name} {self.last_name}'


class Address(models.Model):
    """
    The model for describing the place of reception of a specialist
    """
    specialist = models.ForeignKey(
        Specialist,
        related_name='addresses',
        on_delete=models.CASCADE
    )
    loc_latitude = models.FloatField(verbose_name='Address latitude')
    loc_longitude = models.FloatField(verbose_name='Address longitude')
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.loc_latitude}, {self.loc_longitude}'

    def save(self, **kwargs):
        self.description_en, self.description_ru = translate_field(
            self.description_en, self.description_ru)
        super(Address, self).save()


class Service(models.Model):
    """
    The model for describing the services and prices of a specialist
    """
    class Currency(models.TextChoices):
        USD = 'USD', _('USD')
        EUR = 'EUR', _('EUR')
        RUB = 'RUB', _('RUB')

    specialist = models.ForeignKey(
        Specialist,
        related_name='services',
        on_delete=models.CASCADE
    )
    name_service = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    currency = models.CharField(
        max_length=5,
        choices=Currency.choices,
        default=Currency.USD
    )

    def __str__(self):
        return f'{self.name_service} - {self.price} {self.currency}'

    def save(self, **kwargs):
        self.name_service_en, self.name_service_ru = translate_field(
            self.name_service_en, self.name_service_ru)
        self.description_en, self.description_ru = translate_field(
            self.description_en, self.description_ru)
        super(Service, self).save()
