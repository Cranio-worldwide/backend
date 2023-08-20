from django.db import models
from django.db.transaction import atomic

from apps.specialists.models import TitledModel


class News(TitledModel):
    """
    The model for news published by site staff
    """
    text = models.TextField(verbose_name='News text')
    picture = models.ImageField(
        verbose_name='Picture',
        null=True,
        blank=True,
        upload_to='news/%Y-%m-%d'
    )
    date = models.DateTimeField(
        verbose_name='Date of publishment',
        auto_now_add=True,
    )
    is_published = models.BooleanField(
        verbose_name='Show on site',
        default=True,
    )

    class Meta:
        verbose_name = 'New'
        verbose_name_plural = 'News'
        ordering = ('-date',)


class AboutCranio(TitledModel):
    """The model for static block on Main page."""
    image = models.ImageField(
        verbose_name='Picture',
        upload_to='about_cranio/%Y-%m-%d',
    )
    title = models.CharField(verbose_name='About title', max_length=250)
    text = models.TextField(verbose_name='About')
    link = models.URLField(verbose_name='Link')
    is_published = models.BooleanField(
        verbose_name='Show on main page',
        default=True,
    )

    @atomic
    def save(self, **kwargs):
        """Deactivate other objects if this one is_published."""
        if self.is_published:
            abouts = AboutCranio.objects.exclude(pk=self.pk)
            for object in abouts:
                object.is_published = False
            AboutCranio.objects.bulk_update(abouts, ['is_published'])
        super(AboutCranio, self).save()


class StaticContent(models.Model):
    """The model contating static content for frontend."""
    name = models.SlugField(max_length=50)
    fields_ru = models.JSONField()
    fields_en = models.JSONField()

    class Meta:
        verbose_name = 'Static content file'
        verbose_name_plural = 'Static content files'

    def __str__(self):
        return self.name
