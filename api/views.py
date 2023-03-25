from rest_framework import viewsets

from users.models import Specialists
from .models import Address, Services
from .serializers import (
    AdressSerializers, SpecialistsSerializer, ServicesSerializers
)


class SpecialistsViewSet(viewsets.ModelViewSet):
    """ViewSet for model Specialists."""

    queryset = Specialists.objects.all()
    serializer_class = SpecialistsSerializer


class AdressViewSet(viewsets.ModelViewSet):
    """ViewSet for model Address."""
    queryset = Address.objects.all()
    serializer_class = AdressSerializers


class ServicesViewSet(viewsets.ModelViewSet):
    """ViewSet for model Service."""
    queryset = Services.objects.all()
    serializer_class = ServicesSerializers
