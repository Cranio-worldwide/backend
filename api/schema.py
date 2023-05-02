from drf_yasg import openapi

from cranio.consts import MAX_SEARCH_RADIUS


rad = openapi.Parameter(
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

min_p = openapi.Parameter(
    'min_price', openapi.IN_QUERY,
    description="lower limit for search filter",
    type=openapi.TYPE_INTEGER
)

max_p = openapi.Parameter(
    'max_price', openapi.IN_QUERY,
    description="upper limit for search filter",
    type=openapi.TYPE_INTEGER
)
