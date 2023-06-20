from django.db import models
# from django.utils.translation import gettext_lazy as _

from apps.core.services.translations import translate_field


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

    class Meta:
        verbose_name = 'New'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.description[:15]

    def save(self, **kwargs):
        self.description_en, self.description_ru = translate_field(
            self.description_en, self.description_ru)
        super(News, self).save()


class StaticContent(models.Model):
    """
    The model contating static content for frontend
    """
    name = models.SlugField(max_length=50)
    fields_ru = models.JSONField()
    fields_en = models.JSONField()

    class Meta:
        verbose_name = 'Static content file'
        verbose_name_plural = 'Static content files'

    def __str__(self):
        return self.name
