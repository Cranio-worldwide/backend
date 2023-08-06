from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AddressViewSet, CurrencyViewSet, SearchList, ServiceViewSet,
    SpecialistViewSet,
)

router = DefaultRouter()
router.register('specialists',
                SpecialistViewSet, basename='specialists')
router.register(r'specialists/(?P<specialist_id>[0-9a-f-]+)/addresses',
                AddressViewSet, basename='addresses')
router.register(r'specialists/(?P<specialist_id>[0-9a-f-]+)/services',
                ServiceViewSet, basename='services')
router.register('search', SearchList, basename='search')
router.register('currencies', CurrencyViewSet, basename='currencies')


urlpatterns = [
    path('', include(router.urls)),
]
