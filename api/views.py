from rest_framework import viewsets

from users.models import Specialist
from .models import Address, Service
from .serializers import (
    AdressSerializer, SpecialistSerializer, ServiceSerializer
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
