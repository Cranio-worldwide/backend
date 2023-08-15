from modeltranslation.translator import TranslationOptions, register

from .models import (
    Address, Currency, SpecialistProfile,
)


@register(SpecialistProfile)
class SpecialistProfileTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'about')


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Currency)
class CurrencyTranslationOptions(TranslationOptions):
    fields = ('name',)
