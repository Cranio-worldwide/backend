from googletrans import Translator
from transliterate import translit


def translate_field(field_en, field_ru):
    translator = Translator()
    if not field_en and field_ru:
        translated_obj = translator.translate(field_ru, dest='en', src='ru')
        field_en = translated_obj.text
    if not field_ru and field_en:
        translated_obj = translator.translate(field_en, dest='ru')
        field_ru = translated_obj.text
    return field_en, field_ru


def transliterate_field(field_en, field_ru):
    if not field_en and field_ru:
        field_en = translit(field_ru, reversed=True)
    if not field_ru and field_en:
        field_ru = translit(field_en, 'ru')
    return field_en, field_ru
