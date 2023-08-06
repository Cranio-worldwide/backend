from modeltranslation.translator import TranslationOptions, register

from .models import (
    Address, Currency, Service, SpecialistProfile,
)


@register(SpecialistProfile)
class SpecialistProfileTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'about')


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name_service', 'description')


@register(Currency)
class CurrencyTranslationOptions(TranslationOptions):
    fields = ('name',)
