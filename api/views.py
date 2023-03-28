from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from users.models import Specialist
from .models import Address, Service, Country, News, City
from .serializers import (
    AdressSerializer, SpecialistSerializer, ServiceSerializer, NewsSerializer
)
from .utils import get_geodata, get_user_ip_address, parse_geodata


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
#         country = get_object_or_404(Country, pk=self.kwargs.get('country_id'))
#         return country.cities.all()


class NewsViewSet(viewsets.ModelViewSet):
    """Viewset for model News. Adds/changes - through admin panel."""
    serializer_class = NewsSerializer
    queryset = News.objects.all()


class GeopositionViewSet(viewsets.ViewSet):
    """Viewset for retrieving user geoposition by IP-address from request"""
    def list(self, request):
        ip_address = get_user_ip_address(request)
        geodata = get_geodata(ip_address)
        city, country, coordinates = parse_geodata(request, geodata)
        data = {
            "city": city,
            "country": country,
            "coordinates": coordinates,
        }
        return Response(data)
