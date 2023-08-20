from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (Address, CranioDiploma, CranioInstitute, Currency,
                     Document, Language, ServiceType, Specialist,
                     Specialization, Status)


class StatusInline(admin.TabularInline):
    model = Status


class DiplomaInline(admin.TabularInline):
    model = CranioDiploma


class DocumentInline(admin.TabularInline):
    model = Document


@admin.register(Specialist)
class SpecialistAdmin(TranslationAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name',
                    'status', 'modified')
    list_filter = ('status',)
    inlines = (StatusInline, DiplomaInline, DocumentInline)
    autocomplete_fields = ('languages', 'specializations', 'service_types')

    def status(self, obj):
        return obj.status.stage

    def modified(self, obj):
        return obj.status.modified

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    status.short_description = 'Status'
    modified.short_description = 'Last status update'


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
    list_display = ('id', 'title_ru', 'title_en')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Specialization)
class SpecializationAdmin(TranslationAdmin):
    list_display = ('id', 'title_ru', 'title_en')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(ServiceType)
class ServiceTypeAdmin(TranslationAdmin):
    list_display = ('id', 'title_ru', 'title_en')
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(CranioInstitute)
class CranioInstituteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    empty_value_display = '-пусто-'
