from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Address, Currency, SpecialistProfile


@admin.register(SpecialistProfile)
class SpecialistProfileAdmin(TranslationAdmin):
    list_display = ('id', 'specialist', 'first_name', 'last_name', 'phone')
    search_fields = ('first_name', 'last_name', 'phone')


@admin.register(Address)
class AddressAdmin(TranslationAdmin):
    list_display = ('id', 'specialist', 'loc_latitude', 'loc_longitude',
                    'min_price', 'currency')
    list_filter = ('specialist',)
    search_fields = ('specialist',)
    empty_value_display = '-пусто-'


@admin.register(Currency)
class CurrencyAdmin(TranslationAdmin):
    list_display = ('id', 'slug', 'name')
    empty_value_display = '-пусто-'
