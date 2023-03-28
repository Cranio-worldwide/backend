from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdressViewSet, SpecialistViewSet, ServiceViewSet,
                    CountryViewSet, CityViewSet, NewsViewSet,
                    GeopositionViewSet)


router = DefaultRouter()

router.register('specialists', SpecialistViewSet, basename='specialists')
router.register('address', AdressViewSet, basename='address')
router.register('services', ServiceViewSet, basename='services')
router.register('countries', CountryViewSet, basename='countries')
router.register(r'countries/(?P<country_id>\d+)/cities', CityViewSet,
                basename='cities')
router.register('news', NewsViewSet, basename='news'),
router.register('user_location', GeopositionViewSet, basename='user_location')

urlpatterns = [
    path('v1/', include(router.urls)),
]
