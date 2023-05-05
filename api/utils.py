from http import HTTPStatus
from math import cos, pi

import requests
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import DecimalField, F, Max, Min
from django.db.models.functions import Sqrt
from django.urls import reverse
from googletrans import Translator
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.tokens import RefreshToken
from transliterate import translit

from cranio.consts import (DEFAULT_SEARCH_RADIUS, HALF_CIRCLE, KM_IN_DEGREE,
                           MAX_SEARCH_RADIUS)


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


def filter_qs(queryset, query_params):
    try:
        radius = int(query_params.get(
            'radius', DEFAULT_SEARCH_RADIUS
        ))
        assert radius <= MAX_SEARCH_RADIUS
        assert radius > 0
    except (ValueError, AssertionError):
        raise ParseError(
            f'Enter radius as integer in range from 1 to {MAX_SEARCH_RADIUS}'
        )
    try:
        coordinates = query_params.get('coordinates')
        point_lat, point_lon = map(float, coordinates.split(','))
    except (ValueError, AttributeError):
        raise ParseError('Enter laitude & longitude separated by comma.')
    radius_in_degree = radius / KM_IN_DEGREE
    km_in_lon_degree = cos(point_lat / HALF_CIRCLE * pi) * KM_IN_DEGREE
    queryset = (queryset.filter(
        loc_latitude__gt=(point_lat - radius_in_degree),
        loc_latitude__lt=(point_lat + radius_in_degree),
        loc_longitude__gt=(point_lon - radius_in_degree),
        loc_longitude__lt=(point_lon + radius_in_degree),
    ).annotate(distance=Sqrt(
        (
            (F('loc_latitude') - point_lat) * KM_IN_DEGREE
        ) ** 2 + (
            (F('loc_longitude') - point_lon) * km_in_lon_degree
        ) ** 2,
        output_field=DecimalField(max_digits=4, decimal_places=1)
    )).
        select_related('specialist').
        prefetch_related('specialist__services', 'specialist__addresses').
        annotate(min_price=Min('specialist__services__price')).
        annotate(max_price=Max('specialist__services__price')).
        order_by('distance'))

    min_price_filter = query_params.get('min_price')
    max_price_filter = query_params.get('max_price')
    try:
        if min_price_filter:
            queryset = queryset.filter(max_price__gte=min_price_filter)
        if max_price_filter:
            return queryset.filter(min_price__lte=max_price_filter)
    except ValueError:
        raise ParseError('Prices should be integers')
    return queryset
