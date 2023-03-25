from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdressViewSet, SpecialistsViewSet, ServicesViewSet


router = DefaultRouter()

router.register('specialists', SpecialistsViewSet, basename='specialists')
router.register('address', AdressViewSet, basename='address')
router.register('services', ServicesViewSet, basename='services')

urlpatterns = [
    path('', include(router.urls)),
]
