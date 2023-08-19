from math import cos, pi

from django.db.models import DecimalField, F
from django.db.models.functions import Sqrt
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ParseError

from apps.core.consts import (
    DEFAULT_SEARCH_RADIUS, HALF_CIRCLE, KM_IN_DEGREE, MAX_SEARCH_RADIUS,
)


def clean_radius(radius):
    try:
        radius = int(radius)
        assert 0 < radius <= MAX_SEARCH_RADIUS
        return radius
    except (ValueError, AssertionError):
        raise ParseError(
            _('Enter radius as integer in range from 1'
              ' to ') + f'{MAX_SEARCH_RADIUS}.'
        )


def clean_coordinates(coordinates):
    try:
        coordinates = coordinates.split(',')
        assert len(coordinates) == 2
        return map(float, coordinates)
    except (ValueError, AttributeError, AssertionError):
        raise ParseError(_('Enter laitude & longitude separated by comma.'))


def clean_price_filter(price):
    try:
        price = int(price)
        return price
    except ValueError:
        raise ParseError(_('Prices should be integers'))


def filter_qs(queryset, query_params):
    radius = clean_radius(query_params.get('radius', DEFAULT_SEARCH_RADIUS))
    point_lat, point_lon = clean_coordinates(query_params.get('coordinates'))

    radius_in_degree = radius / KM_IN_DEGREE
    km_in_lon_degree = cos(point_lat / HALF_CIRCLE * pi) * KM_IN_DEGREE
    queryset = (queryset.filter(
        loc_latitude__gt=(point_lat - radius_in_degree),
        loc_latitude__lt=(point_lat + radius_in_degree),
        loc_longitude__gt=(point_lon - radius_in_degree),
        loc_longitude__lt=(point_lon + radius_in_degree),
        specialist__status__stage='ACTIVE')
    )

    min_price = query_params.get('min_price')
    max_price = query_params.get('max_price')
    if min_price:
        min_price = clean_price_filter(min_price)
        queryset = queryset.filter(min_price__gte=min_price)
    if max_price:
        max_price = clean_price_filter(max_price)
        return queryset.filter(min_price__lte=max_price)

    queryset = (
        queryset.
        annotate(
            distance=Sqrt(
                (
                    (F('loc_latitude') - point_lat) * KM_IN_DEGREE
                ) ** 2 + (
                    (F('loc_longitude') - point_lon) * km_in_lon_degree
                ) ** 2,
                output_field=DecimalField(max_digits=4, decimal_places=1)
            )
        ).
        select_related('specialist').
        # prefetch_related('specialist__services', 'specialist__addresses').
        order_by('distance')
    )

    return queryset
