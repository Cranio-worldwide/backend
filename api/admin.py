from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Address, Service, News, StaticContent


class AddressAdmin(TranslationAdmin):
    list_display = ('id', 'specialists_id', 'loc_latitude', 'loc_longitude', )
    search_fields = ('id', 'specialists_id', 'loc_latitude', 'loc_longitude')
    empty_value_display = '-пусто-'


class ServiceAdmin(TranslationAdmin):
    list_display = ('specialists_id', 'name_service', 'price', 'currency')
    search_fields = ('specialists_id', 'name_service', 'price', 'currency')
    empty_value_display = '-пусто-'


class NewsAdmin(TranslationAdmin):
    list_display = ('date', 'description', 'published')
    search_fields = ('date', 'description')
    empty_value_display = '-пусто-'


class StaticContentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Address, AddressAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(StaticContent, StaticContentAdmin)
