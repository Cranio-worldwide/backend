from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import News, StaticContent


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('date', 'description', 'published')
    search_fields = ('date', 'description')
    empty_value_display = '-пусто-'


@admin.register(StaticContent)
class StaticContentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
