from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response


from .filters import StaticContentFilter
from .models import News, StaticContent
from .serializers import (
    NewsSerializer, StaticContentSerializer
)
from .utils import (
    get_geodata, get_user_ip_address, parse_coordinates,
)


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for model News. Adds/changes - through admin panel."""
    serializer_class = NewsSerializer
    queryset = News.objects.all()


class GeopositionViewSet(viewsets.ViewSet):
    """Viewset for reciept of user geoposition by IP-address"""

    def list(self, request):
        ip_address = get_user_ip_address(request)
        geodata = get_geodata(ip_address)
        coordinates = parse_coordinates(geodata)
        data = {"coordinates": coordinates}
        return Response(data)


class StaticContentViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for transfer of multilingual static content to frontend
       Filtering via 'name' parameter: use comma(',') for multiple filter
    """
    serializer_class = StaticContentSerializer
    queryset = StaticContent.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StaticContentFilter
    lookup_field = 'name'
