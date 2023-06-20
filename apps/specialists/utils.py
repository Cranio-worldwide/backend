from math import cos, pi

from django.db.models import DecimalField, F, Max, Min
from django.db.models.functions import Sqrt
from rest_framework.exceptions import ParseError

from apps.core.consts import (
    DEFAULT_SEARCH_RADIUS, HALF_CIRCLE, KM_IN_DEGREE, MAX_SEARCH_RADIUS,
)


def clean_radius(radius):
    try:
        radius = int(radius)
        assert 0 < radius <= MAX_SEARCH_RADIUS
        # assert radius > 0
        return radius
    except (ValueError, AssertionError):
        raise ParseError(
            f'Enter radius as integer in range from 1 to {MAX_SEARCH_RADIUS}'
        )


def clean_coordinates(coordinates):
    try:
        coordinates = map(float, coordinates.split(','))
        return coordinates
    except (ValueError, AttributeError):
        raise ParseError('Enter laitude & longitude separated by comma.')


def clean_price_filter(price):
    try:
        price = int(price)
        return price
    except ValueError:
        raise ParseError('Prices should be integers')


def filter_qs(queryset, query_params):
    radius = clean_radius(query_params.get('radius', DEFAULT_SEARCH_RADIUS))
    point_lat, point_lon = clean_coordinates(query_params['coordinates'])

    radius_in_degree = radius / KM_IN_DEGREE
    km_in_lon_degree = cos(point_lat / HALF_CIRCLE * pi) * KM_IN_DEGREE
    queryset = (
        queryset.
        filter(loc_latitude__gt=(point_lat - radius_in_degree),
               loc_latitude__lt=(point_lat + radius_in_degree),
               loc_longitude__gt=(point_lon - radius_in_degree),
               loc_longitude__lt=(point_lon + radius_in_degree),
               specialist__profile__status='ACTIVE').
        annotate(
            distance=Sqrt(
                (
                    (F('loc_latitude') - point_lat) * KM_IN_DEGREE
                ) ** 2 + (
                    (F('loc_longitude') - point_lon) * km_in_lon_degree
                ) ** 2,
                output_field=DecimalField(max_digits=4, decimal_places=1))
        ).
        # НЕ РАБОТАЕТ АГГРЕГАЦИЯ НА АННОТИРОВАННОЕ ПОЛЕ
        # annotate(is_closest=Case(When(distance=F('min_distance'),then=Value(1)),
        #                          default=Value(0),
        #                          output_field=BooleanField())).
        # filter(distance=Min('specialist__addresses__distance')).
        select_related('specialist').
        prefetch_related('specialist__services', 'specialist__addresses').
        order_by('distance')
        # НЕ РАБОТАЕТ DISTINCT ПРИ АННОТАЦИИ И СОРТИРОВКЕ ПО ДИСТАНЦИИ
        # distinct('specialist')
    )

    queryset = (queryset.
                annotate(min_price=Min('specialist__services__price'))
                .annotate(max_price=Max('specialist__services__price')))

    min_price = query_params.get('min_price')
    max_price = query_params.get('max_price')
    if min_price:
        min_price = clean_price_filter(min_price)
        queryset = queryset.filter(max_price__gte=min_price)
    if max_price:
        max_price = clean_price_filter(max_price)
        return queryset.filter(min_price__lte=max_price)

    return queryset