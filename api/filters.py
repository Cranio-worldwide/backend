from django_filters import rest_framework as filters

from api.models import StaticContent


class StaticContentFilter(filters.FilterSet):
    """Filter for static content via 'name' field"""
    class Meta:
        model = StaticContent
        fields = ('name',)

    def filter_queryset(self, queryset):
        name_filter = self.form.cleaned_data.get('name')
        if name_filter:
            values = name_filter.split(',')
            return queryset.filter(name__in=values)
        return queryset


# class SearchFilter(filters.FilterSet):
#     """Filter for search of specialists"""
#     radius = filters.NumberFilter()
#     coordinates = filters.CharFilter()
#     min_price = filters.NumberFilter()
#     max_price = filters.NumberFilter()

#     class Meta:
#         model = Address
#         fields = ('radius', 'coordinates', 'min_price', 'max_price')

#     def filter_queryset(self, queryset):
#         radius = int(self.request.query_params.get(
#             'radius', DEFAULT_SEARCH_RADIUS
#         ))
#         try:
#             coordinates = self.request.query_params.get('coordinates')
#             point_lat, point_lon = map(float, coordinates.split(','))
#         except (ValueError, AttributeError):
#             raise ValueError('Please enter coordinates separated by comma')
#         radius_in_degree = radius / KM_IN_DEGREE
#         km_in_lon_degree = cos(point_lat / HALF_CIRCLE * pi) * KM_IN_DEGREE
#         queryset = (queryset.filter(
#             loc_latitude__gt=(point_lat - radius_in_degree),
#             loc_latitude__lt=(point_lat + radius_in_degree),
#             loc_longitude__gt=(point_lon - radius_in_degree),
#             loc_longitude__lt=(point_lon + radius_in_degree),
#         ).annotate(distance=Sqrt(
#             (
#                 (F('loc_latitude') - point_lat) * KM_IN_DEGREE
#             ) ** 2 + (
#                 (F('loc_longitude') - point_lon) * km_in_lon_degree
#             ) ** 2,
#             output_field=DecimalField(max_digits=4, decimal_places=1)
#         )).
#             select_related('specialist').
#             prefetch_related('specialist__services', 'specialist__addresses')
#             annotate(min_price=Min('specialist__services__price')).
#             annotate(max_price=Max('specialist__services__price')).
#             order_by('distance'))

#         min_price_filter = self.request.query_params.get('min_price')
#         max_price_filter = self.request.query_params.get('max_price')
#         if min_price_filter:
#             queryset = queryset.filter(max_price__gte=min_price_filter)
#         if max_price_filter:
#             return queryset.filter(min_price__lte=max_price_filter)
#         return queryset
