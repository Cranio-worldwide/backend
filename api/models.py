from django.db import models
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
    loc_latitude = models.DecimalField(max_digits=8, decimal_places=6)
    loc_longitude = models.DecimalField(max_digits=8, decimal_places=6)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.loc_latitude}, {self.loc_longitude}'


class Service(models.Model):
    """
    The model for describing the services and prices of a specialist
    """
    USD = 'USD'
    EUR = 'EUR'
    RUB = 'RUB'

    CURRENCY_CHOICES = (
        (USD, 'USD'),
        (EUR, 'EUR'),
        (RUB, 'RUB')
    )
    specialists_id = models.ForeignKey(
        Specialist,
        related_name='service',
        on_delete=models.CASCADE
    )
    name_service = models.CharField(
        max_length=80, default='visiting a specialist')
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    currency = models.CharField(
        max_length=50,
        choices=CURRENCY_CHOICES,
        default=USD
    )

    def __str__(self):
        return f'{self.name_service}, {self.price}, {self.currency}'
