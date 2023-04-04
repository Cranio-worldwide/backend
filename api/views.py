from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Specialist
from .models import Address, Service, News
from .serializers import (
    AdressSerializer, SpecialistSerializer, ServiceSerializer, NewsSerializer,
    UserSerializer
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
    """Viewset for retrieving user geoposition by IP-address from request"""

    def list(self, request):
        ip_address = get_user_ip_address(request)
        geodata = get_geodata(ip_address)
        coordinates = parse_coordinates(geodata)
        data = {"coordinates": coordinates}
        return Response(data)


class RegisterView(APIView):
    """Viewset for users' authorization with JWT."""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'data': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
