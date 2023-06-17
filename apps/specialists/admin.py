from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Address, Currency, Service, SpecialistProfile


@admin.register(SpecialistProfile)
class SpecialistProfileAdmin(TranslationAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'phone',
                    'diploma_issuer', 'diploma_recipient')
    search_fields = ('first_name', 'last_name', 'phone',
                     'diploma_issuer', 'diploma_recipient')

@admin.register(Address)
class AddressAdmin(TranslationAdmin):
    list_display = ('id', 'specialist', 'loc_latitude', 'loc_longitude', )
    search_fields = ('specialist',)
    empty_value_display = '-пусто-'


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('specialist', 'name_service', 'price', 'currency')
    search_fields = ('specialist', 'name_service')
    empty_value_display = '-пусто-'


@admin.register(Currency)
class CurrencyAdmin(TranslationAdmin):
    list_display = ('slug', 'name')
    empty_value_display = '-пусто-'