from drf_yasg import openapi

from apps.core.consts import MAX_SEARCH_RADIUS


radius = openapi.Parameter(
    'radius', openapi.IN_QUERY,
    description=("search radius in km, default=50km, "
                 f"range: 1 -> {MAX_SEARCH_RADIUS}"),
    type=openapi.TYPE_INTEGER
)

coords = openapi.Parameter(
    'coordinates', openapi.IN_QUERY,
    description=("coordinates of search center in degrees, "
                 "format: 'latitude, longintude'"),
    type=openapi.TYPE_STRING
)

min_price = openapi.Parameter(
    'min_price', openapi.IN_QUERY,
    description="lower limit for search filter",
    type=openapi.TYPE_INTEGER
)

max_price = openapi.Parameter(
    'max_price', openapi.IN_QUERY,
    description="upper limit for search filter",
    type=openapi.TYPE_INTEGER
)
