from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from modeltranslation.admin import TranslationAdmin

from .models import SpecialistData, Address, Service


@admin.register(SpecialistData)
class SpecialistDataAdmin(TranslationAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'phone',
                    'diploma_issuer', 'diploma_recipient')
    # search_fields = ('id', 'first_name', 'last_name', 'phone',
    #                  'diploma_issuer', 'diploma_recipient')

@admin.register(Address)
class AddressAdmin(TranslationAdmin):
    list_display = ('id', 'specialist', 'loc_latitude', 'loc_longitude', )
    search_fields = ('id', 'specialist', 'loc_latitude', 'loc_longitude')
    empty_value_display = '-пусто-'


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('specialist', 'name_service', 'price', 'currency')
    search_fields = ('specialist', 'name_service', 'price', 'currency')
    empty_value_display = '-пусто-'
