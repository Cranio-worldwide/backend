from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from apps.core.services.translations import (
    translate_field, transliterate_field,
)
from apps.users.models import CustomUser

from .managers import SpecialistManager
from .validators import validate_year


class Specialist(CustomUser):
    """Class for creating a user: Specialists."""
    role = CustomUser.Role.SPECIALIST

    objects = SpecialistManager()

    class Meta:
        proxy = True
        verbose_name = 'Specialist'
        verbose_name_plural = 'Specialists'

    def __str__(self):
        return self.email


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'SPECIALIST':
        SpecialistProfile.objects.create(specialist=instance)


class SpecialistProfile(models.Model):
    """The  model for specialist profile: 1to1 with Specialist."""


    specialist = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile'
    )
    first_name = models.CharField(
        verbose_name='First name', blank=True, max_length=150
    )
    last_name = models.CharField(
        verbose_name='Last name', blank=True, max_length=150
    )
    photo = models.ImageField(
        verbose_name="Specialist's photo",
        null=True,
        blank=True,
        upload_to='photo/%Y-%m-%d',
    )
    about = models.TextField(
        verbose_name='About specialist',
        blank=True,
        max_length=2000,
    )
    phone = models.CharField(
        verbose_name='Phone number',
        max_length=17,
        unique=True,
        blank=True,
        null=True
    )
    speciality = models.CharField(
        verbose_name='Speciality',
        max_length=100,
    )
    specialization = models.ForeignKey(

    )


    class Meta:
        verbose_name = 'Specialist Profile'
        verbose_name_plural = 'Specialists Profiles'

    def save(self, **kwargs):
        """Translate blank about, transliterate first & last name."""
        self.first_name_en, self.first_name_ru = transliterate_field(
            self.first_name_en, self.first_name_ru)
        self.last_name_en, self.last_name_ru = transliterate_field(
            self.last_name_en, self.last_name_ru)
        self.about_en, self.about_ru = translate_field(
            self.about_en, self.about_ru)
        super(SpecialistProfile, self).save()

    def __str__(self):
        return f'{self.specialist}: {self.first_name} {self.last_name}'

    def clean(self):
        """
        Demands filling comments if corrections by specialist are required.
        Cleans comments if approval is passed.
        """
        if (self.status == self.Status.CORRECTING and not
                self.approver_comments):
            raise ValidationError(_('Please comment the status.'))
        if (self.approver_comments and self.status not in [
                self.Status.CORRECTING, self.Status.CHECKING]):
            self.approver_comments = ''


class Address(models.Model):
    """The model for specialist's place of reception."""
    specialist = models.ForeignKey(
        Specialist,
        related_name='addresses',
        on_delete=models.CASCADE
    )
    loc_latitude = models.FloatField(verbose_name='Address latitude')
    loc_longitude = models.FloatField(verbose_name='Address longitude')
    description = models.TextField(
        verbose_name='Details of address',
        blank=True,
    )
    min_price = models.IntegerField(
        verbose_name='Minimal price',
        validators=[MinValueValidator(1, _('Value should be larger than 0.'))]
    )
    currency = models.ForeignKey(
        'Currency',
        on_delete=models.SET_DEFAULT,
        default=3,
        verbose_name='Currency',
    )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.loc_latitude}, {self.loc_longitude}'

    def save(self, **kwargs):
        """Translating blank description field"""
        self.description_en, self.description_ru = translate_field(
            self.description_en, self.description_ru)
        super(Address, self).save()


class Currency(models.Model):
    """The Currency model."""
    slug = models.SlugField(verbose_name='Currency slug')
    name = models.CharField(verbose_name='Currency name', max_length=20)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.slug


class CranioInstitute(models.Model):
    name = models.CharField(verbose_name='Cranio organization', max_length=250)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name


class Status(models.Model):
    class Stage(models.TextChoices):
        FILLING = 'FILLING', _('Filling out the application.')
        CHECK = 'CHECK', _('Pending diploma confirmation.')
        EDIT = 'EDIT', _('Corrections are required.')
        PAYING = 'PAYING', _('Pending payment.')
        ACTIVE = 'ACTIVE', _('Active account.')

    specialist = models.OneToOneField(
        Specialist,
        on_delete=models.CASCADE,
        related_name='status',
    )
    stage = models.CharField(
        verbose_name='Status of specialist',
        max_length=50,
        choices=Stage.choices,
        default=Stage.FILLING,
    )
    comments = models.TextField(
        verbose_name='Admin comments for corrections',
        blank=True,
    )
    modified = models.DateTimeField(
        verbose_name='Last status update',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Specialist Status'
        verbose_name_plural = 'Specialists Statuses'

    def __str__(self):
        return self.stage


class CranioEducation(models.Model):

    specialist = models.OneToOneField(
        Specialist,
        on_delete=models.CASCADE,
        related_name='education',
    )
    diploma_issuer = models.ForeignKey(
        CranioInstitute,
        on_delete=models.SET_NULL,
        null=True,
    )
    diploma_recipient = models.CharField(
        verbose_name='Name of diploma recipient mentioned in diploma',
        max_length=100,
    )
    diploma_year = models.SmallIntegerField(
        verbose_name='Year of diploma issue'
    )
    document = models.FileField(
        verbose_name='Scanned document',
        null=True,
        blank=True,
        upload_to='diplomas/%Y-%m-%d',
    )
