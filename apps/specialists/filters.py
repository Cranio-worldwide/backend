from math import cos, pi

from django.db.models import DecimalField, F, Max, Min
from django.db.models.functions import Sqrt
from rest_framework.exceptions import ParseError

from apps.core.consts import (DEFAULT_SEARCH_RADIUS, HALF_CIRCLE, KM_IN_DEGREE,
                              MAX_SEARCH_RADIUS)


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
