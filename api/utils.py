import requests
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from googletrans import Translator
from http import HTTPStatus
from rest_framework_simplejwt.tokens import RefreshToken
from transliterate import translit


def get_user_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip_address = user_ip_address.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    print(ip_address)
    return ip_address


def get_geodata(ip_address):
    if ip_address == '127.0.0.1' or ip_address.startswith('172'):
        endpoints = (
            # temporary solution for development process
            'https://ipapi.co/json/',
            'https://api.ipgeolocation.io/ipgeo?'
            'apiKey=2b3f60044ccf4af3b5b67882e3c2172f',
        )
    else:
        endpoints = (
            # these endpoints provide 1000 free requests/day, more to be added
            f'https://ipapi.co/{ip_address}/json/',
            'https://api.ipgeolocation.io/ipgeo?'
            f'apiKey=2b3f60044ccf4af3b5b67882e3c2172f&ip={ip_address}',
        )
    for endpoint in endpoints:
        response = requests.get(endpoint)
        if response.status_code == HTTPStatus.OK:
            return response.json()
    return None


# def parse_geodata(request, geodata):
#     city, country = geodata.get('city'), geodata.get('country_name')
#     coordinates = f"{geodata.get('latitude')}, {geodata.get('longitude')}"
#     lang_prefix = request.path[1:3]
#     if lang_prefix != 'en':
#         translator = Translator()
#         location = f"{geodata.get('city')}|{geodata.get('country_name')}"
#         location = translator.translate(location, dest=lang_prefix)
#         city, country = [name.strip() for name in location.text.split('|')]
#     return city, country, coordinates


def parse_coordinates(geodata):
    return f"{geodata.get('latitude')}, {geodata.get('longitude')}"


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


def send_verification_email(request, user, language):
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    url_path = reverse('verify_email')
    absurl = 'http://' + current_site + url_path + '?token=' + str(token)
    subject = settings.CONSTANTS['EMAIL_SUBJECT']
    text = settings.CONSTANTS["EMAIL_MESSEGE"]

    if language == 'ru':
        translator = Translator()
        subject = translator.translate(subject, dest='ru', src='en')
        subject = subject.text
        text = translator.translate(text, dest='ru', src='en')
        text = text.text

    email_body = (
        f'{user.email} \n'
        f'{text} \n' + absurl
    )

    email = EmailMessage(
        to=[user.email],
        subject=subject,
        body=email_body
    )
    email.send()
