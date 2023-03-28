from django.db import models
from django.utils.translation import gettext_lazy as _

from api.utils import translate_field
from users.models import Specialist


class Address(models.Model):
    """
    The model for describing the place of reception of a specialist
    """
    specialists_id = models.ForeignKey(
        Specialist,
        related_name='address',
        on_delete=models.CASCADE
    )
    loc_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    loc_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.loc_latitude}, {self.loc_longitude}'

    def save(self, **kwargs):
        self.description_en, self.description_ru = \
            translate_field(self.description_en, self.description_ru)
        super(Address, self).save()


class Service(models.Model):
    """
    The model for describing the services and prices of a specialist
    """
    USD = _('USD')
    EUR = _('EUR')
    RUB = _('RUB')

    CURRENCY_CHOICES = (
        (USD, USD),
        (EUR, EUR),
        (RUB, RUB)
    )
    specialists_id = models.ForeignKey(
        Specialist,
        related_name='service',
        on_delete=models.CASCADE
    )
    name_service = models.CharField(
        max_length=80, default=_('Visit a specialist'))
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    currency = models.CharField(
        max_length=50,
        choices=CURRENCY_CHOICES,
        default=USD
    )

    def __str__(self):
        return f'{self.name_service}, {self.price}, {self.currency}'

    def save(self, **kwargs):
        self.name_service_en, self.name_service_ru = \
            translate_field(self.name_service_en, self.name_service_ru)
        self.description_en, self.description_ru = \
            translate_field(self.description_en, self.description_ru)
        super(Service, self).save()


class Country(models.Model):
    """
    The model for countries for user geopositioning
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    The model for cities for user geopositioning
    """
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities',
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name

    def coordinates(self):
        return (float(self.latitude), float(self.longitude))


class News(models.Model):
    """
    The model for news published by site staff
    """
    description = models.TextField()
    picture = models.ImageField(
        null=True,
        blank=True,
        upload_to='news/%Y-%m-%d'
    )
    date = models.DateField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.description[:15]

    def save(self, **kwargs):
        self.description_en, self.description_ru = \
            translate_field(self.description_en, self.description_ru)
        super(News, self).save()
