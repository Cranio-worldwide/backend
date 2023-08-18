from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Address, CranioInstitute, Currency, Specialist, Language, ServiceType, Specialization


@admin.register(Specialist)
class SpecialistAdmin(TranslationAdmin):
    list_display = ('id', 'user', 'speciality', 'status')
    list_filter = ('status',)

    def status(self, obj):
        return obj.status.stage

    status.short_description = 'Status'


@admin.register(Address)
class AddressAdmin(TranslationAdmin):
    list_display = ('id', 'specialist', 'loc_latitude', 'loc_longitude',
                    'min_price', 'currency')
    search_fields = ('specialist',)
    empty_value_display = '-пусто-'


@admin.register(Currency)
class CurrencyAdmin(TranslationAdmin):
    list_display = ('id', 'slug', 'name')
    empty_value_display = '-пусто-'


@admin.register(Language)
class LanguageAdmin(TranslationAdmin):
    list_display = ('id', 'title')
    empty_value_display = '-пусто-'


@admin.register(Specialization)
class SpecializationAdmin(TranslationAdmin):
    list_display = ('id', 'title')
    empty_value_display = '-пусто-'


@admin.register(ServiceType)
class ServiceTypeAdmin(TranslationAdmin):
    list_display = ('id', 'title')
    empty_value_display = '-пусто-'


@admin.register(CranioInstitute)
class CranioInstituteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    empty_value_display = '-пусто-'
