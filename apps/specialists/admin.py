from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Address, Currency, Service, SpecialistProfile


@admin.register(SpecialistProfile)
class SpecialistProfileAdmin(TranslationAdmin):
    list_display = ('id', 'specialist', 'first_name', 'last_name', 'phone',
                    'diploma_issuer', 'diploma_recipient')
    search_fields = ('first_name', 'last_name', 'phone',
                     'diploma_issuer', 'diploma_recipient')


@admin.register(Address)
class AddressAdmin(TranslationAdmin):
    list_display = ('id', 'specialist', 'loc_latitude', 'loc_longitude', )
    list_filter = ('specialist',)
    search_fields = ('specialist',)
    empty_value_display = '-пусто-'


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('id', 'specialist', 'name_service', 'price', 'currency')
    list_filter = ('specialist',)
    search_fields = ('specialist', 'name_service')
    empty_value_display = '-пусто-'


@admin.register(Currency)
class CurrencyAdmin(TranslationAdmin):
    list_display = ('id', 'slug', 'name')
    empty_value_display = '-пусто-'
