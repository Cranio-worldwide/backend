import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language_from_request
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.models import Specialist
from .models import News, StaticContent
from .serializers import (
    AdressSerializer, SpecialistSerializer, ServiceSerializer, NewsSerializer,
    SpecialistCreateSerializer, StaticContentSerializer
)
from .utils import (
    get_geodata, get_user_ip_address, parse_coordinates,
    send_verification_email
)


class SpecialistViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, mixins.ListModelMixin,
                        GenericViewSet):
    """ViewSet for model Specialists."""
    queryset = Specialist.objects.all()
    serializer_class = SpecialistSerializer


class AdressViewSet(viewsets.ModelViewSet):
    """ViewSet for model Address."""
    serializer_class = AdressSerializer

    def get_specialist(self):
        return get_object_or_404(Specialist,
                                 pk=self.kwargs.get('specialist_id'))

    def get_queryset(self):
        return self.get_specialist().addresses.all()

    def perform_create(self, serializer):
        serializer.save(specialist=self.get_specialist())


class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for model Service."""
    serializer_class = ServiceSerializer

    def get_specialist(self):
        return get_object_or_404(Specialist,
                                 pk=self.kwargs.get('specialist_id'))

    def get_queryset(self):
        return self.get_specialist().services.all()

    def perform_create(self, serializer):
        serializer.save(specialist=self.get_specialist())


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


class StaticContentViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for transfer of multilingual static content to frontend"""
    serializer_class = StaticContentSerializer
    queryset = StaticContent.objects.all()
    lookup_field = 'name'
