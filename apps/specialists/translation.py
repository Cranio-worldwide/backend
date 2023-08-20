from modeltranslation.translator import TranslationOptions, register

from .models import (
    Address, Currency, Specialist, Language, Specialization, ServiceType
)


@register(Specialist)
class SpecialistTranslationOptions(TranslationOptions):
    fields = ('about', 'speciality')


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Currency)
class CurrencyTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Specialization)
class SpecializationTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(ServiceType)
class ServiceTypeTranslationOptions(TranslationOptions):
    fields = ('title',)
