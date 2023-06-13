from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import LimitOffsetPagination

from .models import Address, Specialist
from .schema import rad, coords, max_p, min_p
from .serializers import (
    AddressSerializer, FullSpecialistSerializer,
    ServiceSerializer, SearchSerializer
)
from .utils import filter_qs


class SpecialistViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin, GenericViewSet):
    """ViewSet for model Specialists."""
    queryset = Specialist.objects.prefetch_related('addresses', 'services')
    serializer_class = FullSpecialistSerializer
    


class AbstractAttributeViewSet(viewsets.ModelViewSet):
    """Abstract class for Spec attributes: Addresses & Services"""
    def get_specialist(self):
        return get_object_or_404(Specialist,
                                 pk=self.kwargs.get('specialist_id'))

    def perform_create(self, serializer):
        serializer.save(specialist=self.request.user)


class AddressViewSet(AbstractAttributeViewSet):
    """ViewSet for model Address."""
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.get_specialist().addresses.all()


class ServiceViewSet(AbstractAttributeViewSet):
    """ViewSet for model Service."""
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return self.get_specialist().services.all()


class SearchList(mixins.ListModelMixin, GenericViewSet):
    """Viewset for search of specialists."""
    serializer_class = SearchSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = SearchFilter
    # queryset = Address.objects.all()
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(manual_parameters=[rad, coords, max_p, min_p])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        params = self.request.query_params
        queryset = Address.objects.all()
        return filter_qs(queryset, params)
