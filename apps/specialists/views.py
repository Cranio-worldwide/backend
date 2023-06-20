from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .utils import filter_qs
from .models import Address, Currency, Specialist
from .permissions import IsSpecialistOrReadOnly
from .schema import coords, max_price, min_price, radius
from .serializers import (
    AddressSerializer, CurrencySerializer, FullProfileSerializer,
    FullSpecialistSerializer, SearchSerializer, ServiceSerializer,
)


class SpecialistViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """ViewSet for model Specialists."""
    queryset = Specialist.objects.prefetch_related('addresses', 'services')
    serializer_class = FullSpecialistSerializer
    permission_classes = (IsSpecialistOrReadOnly,)

    @action(methods=['GET', 'PATCH'], detail=True, url_path='profile')
    def specialists_profile(self, request, pk):
        specialist = get_object_or_404(Specialist, pk=pk)

        if request.method == 'GET':
            serializer = FullProfileSerializer(specialist.profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if specialist != request.user:
            return Response()
        serializer = FullProfileSerializer(
            specialist.profile, data=request.data, partial=True,
            context={'request': request, 'spec_id': pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AbstractAttributeViewSet(viewsets.ModelViewSet):
    """Abstract class for Spec attributes: Addresses & Services"""
    permission_classes = (IsSpecialistOrReadOnly,)

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


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for model Currency."""
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


class SearchList(mixins.ListModelMixin, GenericViewSet):
    """Viewset for search of specialists."""
    serializer_class = SearchSerializer
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(manual_parameters=[radius, coords,
                                            max_price, min_price])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        params = self.request.query_params
        queryset = Address.objects.all()
        # return filter_qs(queryset, params)
        # НЕ ПОЛУЧИЛОСЬ НИЧЕГО ЛУЧШЕ - СМ. UTILS.PY
        queryset = list(filter_qs(queryset, params))
        seen_specialists, output = set(), []
        for address in queryset:
            if address.specialist not in seen_specialists:
                output.append(address)
                seen_specialists.add(address.specialist)
        return output
