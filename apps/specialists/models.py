from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.services.translations import translate_field
from apps.users.models import CustomUser

from .validators import validate_year


class Specialist(models.Model):
    """The  model for specialist profile: 1to1 with Specialist."""
    id = models.UUIDField(primary_key=True)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='profile'
    )
    about = models.TextField(verbose_name='About specialist', blank=True)
    speciality = models.CharField(
        verbose_name='Speciality',
        max_length=100,
        blank=True,
    )
    languages = models.ManyToManyField(
        'Language', blank=True,
    )
    specializations = models.ManyToManyField(
        'Specialization', blank=True,
    )
    service_types = models.ManyToManyField(
        'ServiceType', blank=True,
    )

    class Meta:
        verbose_name = 'Specialist Profile'
        verbose_name_plural = 'Specialists Profiles'

    def save(self, **kwargs):
        """Translate blank about, transliterate first & last name."""
        if not self.pk:
            self.id = self.user.id
        self.about_en, self.about_ru = translate_field(
            self.about_en, self.about_ru)
        self.speciality_en, self.speciality_ru = translate_field(
            self.speciality_en, self.speciality_ru)
        super(Specialist, self).save()

    def __str__(self):
        return f'Specialist {self.user}'


class Currency(models.Model):
    """The Currency model."""
    slug = models.SlugField(verbose_name='Currency slug')
    name = models.CharField(verbose_name='Currency name', max_length=20)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.slug


class Address(models.Model):
    """The model for Specialist's place of reception."""
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


class Status(models.Model):
    """Model for status of Specialist's Account"""
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
    comments = models.CharField(
        verbose_name='Admin comments for corrections',
        blank=True,
        max_length=200,
    )
    modified = models.DateTimeField(
        verbose_name='Last status update',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Specialist Status'
        verbose_name_plural = 'Specialists Statuses'

    def __str__(self):
        return self.stage

    def clean(self):
        """
        Demands filling comments if corrections by specialist are required.
        Cleans comments if approval is passed.
        """
        if self.stage == self.Stage.EDIT and not self.comments:
            raise ValidationError(_('Please comment the status.'))
        if (self.comments and self.stage not in [
                    self.Stage.EDIT, self.Stage.CHECK
                ]):
            self.approver_comments = ''


class CranioDiploma(models.Model):
    """Model with data about Specialist's Cranio diploma."""
    specialist = models.OneToOneField(
        Specialist,
        on_delete=models.CASCADE,
        related_name='diploma',
    )
    organization = models.ForeignKey(
        'CranioInstitute',
        on_delete=models.SET_NULL,
        null=True,
    )
    year = models.SmallIntegerField(
        verbose_name='Year of diploma issue',
        validators=[validate_year],
    )
    file = models.FileField(
        verbose_name='Scanned diploma',
        upload_to='diplomas/%Y-%m-%d',
    )

    class Meta:
        verbose_name = 'Education data'
        verbose_name_plural = 'Education datas'

    def __str__(self):
        return f'Diploma of {self.specialist}'


class TitledModel(models.Model):
    """Abstract model with unique title."""
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class Specialization(TitledModel):
    """Model for Specialists' specialization tags."""

    class Meta:
        verbose_name = 'Specialization'
        verbose_name_plural = 'Specializations'


class Language(TitledModel):
    """Model for Specialists' languages spoken."""

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'


class ServiceType(TitledModel):
    class Meta:
        verbose_name = "Type of services"
        verbose_name_plural = 'Types of services'


class CranioInstitute(TitledModel):
    """Model for Cranio educational organizations."""
    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'


class Document(models.Model):
    """Model for Specialists' documents/attachments."""
    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.CASCADE,
        related_name='documents',
    )
    file = models.FileField(
        verbose_name='Scanned document',
        upload_to='diplomas/%Y-%m-%d',
    )

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return f'Document of {self.specialist}'
