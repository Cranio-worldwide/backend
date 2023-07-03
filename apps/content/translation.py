from modeltranslation.translator import register, TranslationOptions

from .models import News, AboutCranio


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(AboutCranio)
class AboutCranioTranslationOptions(TranslationOptions):
    fields = ('text',)
