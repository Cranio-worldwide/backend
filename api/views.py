from rest_framework import viewsets
from rest_framework.response import Response

from users.models import Specialist
from .models import Address, Service, News, StaticContent
from .serializers import (
    AdressSerializer, SpecialistSerializer, ServiceSerializer, NewsSerializer,
    StaticContentSerializer
)
from .utils import get_geodata, get_user_ip_address, parse_coordinates


class SpecialistViewSet(viewsets.ModelViewSet):
    """ViewSet for model Specialists."""

    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


class AdressViewSet(viewsets.ModelViewSet):
    """ViewSet for model Address."""
    queryset = Address.objects.all()
    serializer_class = AdressSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for model Service."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


# class CountryViewSet(viewsets.ReadOnlyModelViewSet):
#     """Viewset for model Country. Adds/changes - through admin panel."""
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer


# class CityViewSet(viewsets.ReadOnlyModelViewSet):
#     """Viewset for model Country. Adds/changes - through admin panel."""
#     serializer_class = CitySerializer

#     def get_queryset(self):
#       country = get_object_or_404(Country, pk=self.kwargs.get('country_id'))
#         return country.cities.all()


class NewsViewSet(viewsets.ModelViewSet):
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
    """Viewset for transfer of multilingual static content to frontend"""
    serializer_class = StaticContentSerializer
    queryset = StaticContent.objects.all()
    lookup_field = 'name'

    # def get_serializer_class(self):
    #     if self.request.path[1:3] == 'en':
    #         return EnStaticContentSerializer
    #     return RuStaticContentSerializer
