import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language_from_request
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Specialist
from .models import Address, Service, News
from .serializers import (
    AdressSerializer, SpecialistSerializer, ServiceSerializer, NewsSerializer,
    SpecialistCreateSerializer
)
from .utils import (
    get_geodata, get_user_ip_address, parse_coordinates,
    send_verification_email
)


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
    """Viewset for users' registaration with JWT."""

    serializer_class = SpecialistCreateSerializer

    def post(self, request):
        language = get_language_from_request(request, check_path=True)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = get_object_or_404(
            Specialist,
            email=serializer.data['email'])

        send_verification_email(request, user, language)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    """Viewset for email verification with JWT."""

    def get(self, request):
        token = request.GET.get('token')
        try:
            data = jwt.decode(token, settings.SECRET_KEY)
            user = get_object_or_404(Specialist, id=data['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                data = {
                    'email': settings.CONSTANTS['EMAIL_SUCCESS_MESSEGE']
                }

                return Response(data, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            data = {
                'error': settings.CONSTANTS['TOKEN_EXPIRED']
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            data = {
                'error': settings.CONSTANTS['TOKEN_INVALID']
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
