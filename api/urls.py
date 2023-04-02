from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdressViewSet, SpecialistViewSet, ServiceViewSet,
                    NewsViewSet, GeopositionViewSet, StaticContentViewSet)


router = DefaultRouter()

router.register('specialists', SpecialistViewSet, basename='specialists')
router.register('address', AdressViewSet, basename='address')
router.register('services', ServiceViewSet, basename='services')
# router.register('countries', CountryViewSet, basename='countries')
# router.register(r'countries/(?P<country_id>\d+)/cities', CityViewSet,
#                 basename='cities')
router.register('news', NewsViewSet, basename='news'),
router.register('me', GeopositionViewSet, basename='me')
router.register('static', StaticContentViewSet, basename='static')

urlpatterns = [
    path('v1/', include(router.urls)),
]
