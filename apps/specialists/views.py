from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .utils import filter_qs
from .mixins import SpecBasedMixin
from .models import Address, Currency, Specialist, Language, Specialization, SpecLanguage, SpecSpecialization
from .permissions import IsSpecialistOrReadOnly
from .schema import coords, max_price, min_price, radius
from .serializers import (
    AddressSerializer, CurrencySerializer, FullProfileSerializer,
    FullSpecialistSerializer, SearchSerializer, LanguageSerializer, SpecializationSerializer, SpecLanguageSerializer, SpecSpecializationSerializer
)


class SpecialistViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """Registered Specialists."""
    queryset = Specialist.objects.prefetch_related('addresses')
    serializer_class = FullSpecialistSerializer
    permission_classes = (IsSpecialistOrReadOnly,)

    @action(methods=['GET', 'PATCH'], detail=True, url_path='profile')
    def specialists_profile(self, request, pk):
        specialist = get_object_or_404(Specialist, pk=pk)

        if request.method == 'GET':
            serializer = FullProfileSerializer(specialist.profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # if specialist != request.user:
        #     return Response()
        serializer = FullProfileSerializer(
            specialist.profile, data=request.data, partial=True,
            context={'request': request, 'spec_id': pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST', 'GET'], detail=True)
    def languages(self, request, user_id):
        request.data['specialist_id'] = user_id
        if request.method == 'GET':
            queryset = request.user.languages.all()
            serializer = SpecLanguageSerializer(queryset, many=True, context={'view': self, 'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = SpecLanguageSerializer(data=request.data, many=True, context={'view': self, 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    # @action(methods=['POST', 'DELETE'], detail=True)
    # def specializations(self, request, pk):
    #     user = request.user
    #     serializer = SpecSpecializationSerializer(data=request.data, context={'view': self, 'request': request})
    #     if request.method == 'POST':
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     specialization = request.data.get('title')
    #     deleted, _ = SpecSpecialization.objects.filter(specialization__title=specialization, specialist=user).delete()
    #     if deleted:
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response(status=status.HTTP_404_NOT_FOUND)


class AbstractAttributeViewSet(viewsets.ModelViewSet):
    """Abstract class for Spec attributes: Addresses, Documents."""
    permission_classes = (IsSpecialistOrReadOnly,)

    def get_specialist(self):
        return get_object_or_404(Specialist,
                                 pk=self.kwargs.get('specialist_id'))

    def perform_create(self, serializer):
        serializer.save(specialist=self.request.user)


class AddressViewSet(SpecBasedMixin, viewsets.ModelViewSet):
    """Specialist's Addresses."""
    serializer_class = AddressSerializer

    def get_queryset(self):
        return self.get_specialist().addresses.all()


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """Available Currencies."""
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """Available Languages."""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    """Specialist's available specializations."""
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


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
        # return filter_qs(queryset, params)
        # НЕ ПОЛУЧИЛОСЬ НИЧЕГО ЛУЧШЕ УДАЛЕНИЯ ДУБЛЕЙ ПО СПЕЦУ - СМ. UTILS.PY
        queryset = list(filter_qs(queryset, params))
        seen_specialists, output = set(), []
        for address in queryset:
            if address.specialist not in seen_specialists:
                output.append(address)
                seen_specialists.add(address.specialist)
        return output
