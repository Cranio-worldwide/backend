from modeltranslation.translator import register, TranslationOptions
from users.models import Specialist
from api.models import Address, Service, News


@register(Specialist)
class SpecialistTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'about')


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name_service', 'description')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('description',)


# @register(Country)
# class CountryTranslationOptions(TranslationOptions):
#     fields = ('name',)


# @register(City)
# class CityTranslationOptions(TranslationOptions):
#     fields = ('name',)
