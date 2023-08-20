from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import AboutCranio, News, StaticContent


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('id', 'date', 'title', 'is_published')
    search_fields = ('date', 'title', 'text')
    empty_value_display = '-пусто-'


@admin.register(AboutCranio)
class AboutCranioAdmin(TranslationAdmin):
    list_display = ('id', 'text', 'title', 'is_published')
    empty_value_display = '-пусто-'


@admin.register(StaticContent)
class StaticContentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
