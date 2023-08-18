from modeltranslation.translator import TranslationOptions, register

from .models import (CustomUser)


@register(CustomUser)
class CustomUserTranslationOptions(TranslationOptions):
    fields = ('first_name', 'middle_name', 'last_name')
