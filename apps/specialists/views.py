from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import LanguageFilter, SpecializationFilter
from .mixins import SpecBasedMixin
from .models import (Address, CranioDiploma, Currency, Language, Specialist,
                     Specialization, Status)
from .permissions import IsSpecialistOrReadOnly
from .schema import coords, max_price, min_price, radius
from .serializers import (AddressSerializer, CranioDiplomaSerializer,
                          CurrencySerializer, DocumentSerializer,
                          LanguageSerializer, SearchSerializer,
                          SpecialistSerializer, SpecializationSerializer,
                          StatusSerializer)
from .utils import filter_qs


class SpecialistViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        GenericViewSet):
    """Registered Specialists."""
    queryset = Specialist.objects.prefetch_related('addresses')
    serializer_class = SpecialistSerializer
    permission_classes = (IsSpecialistOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @action(methods=['GET'], detail=True)
    def diploma(self, request, pk):
        """Specialist's Cranio diploma data."""
        diploma = get_object_or_404(CranioDiploma, specialist_id=pk)
        serializer = CranioDiplomaSerializer(diploma)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False,
            permission_classes=(IsAuthenticated,))
    def verify_diploma(self, request):
        """Sending Specialist's Cranio diploma for verification."""
        serializer = CranioDiplomaSerializer(
            data=request.data,
            context={'view': self, 'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def profile_status(self, request, pk):
        """Status of Specilist's profile on site."""
        profile_status = get_object_or_404(Status, specialist_id=pk)
        serializer = StatusSerializer(profile_status)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressViewSet(SpecBasedMixin, viewsets.ModelViewSet):
    """Specialist's Addresses."""
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.get_specialist().addresses.all()


class DocumentViewSet(SpecBasedMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, mixins.ListModelMixin,
                      mixins.RetrieveModelMixin, GenericViewSet):
    """Specialist's Documents."""
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return self.get_specialist().documents.all()


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """Available Currencies."""
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """Available Languages."""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filterset_class = LanguageFilter


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    """Specialist's available specializations."""
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    filterset_class = SpecializationFilter


class SearchList(mixins.ListModelMixin, GenericViewSet):
    """Search of specialists."""
    serializer_class = SearchSerializer
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(manual_parameters=[radius, coords,
                                            max_price, min_price])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        params = self.request.query_params
        queryset = Address.objects.all()
        return filter_qs(queryset, params)
