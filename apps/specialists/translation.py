from modeltranslation.translator import register, TranslationOptions

from apps.specialists.models import SpecialistData, Address, Service


@register(SpecialistData)
class SpecialistDataTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'about')


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name_service', 'description')
