from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdressViewSet, SpecialistViewSet, ServiceViewSet


router = DefaultRouter()

router.register('specialists', SpecialistViewSet, basename='specialists')
router.register('address', AdressViewSet, basename='address')
router.register('services', ServiceViewSet, basename='services')

urlpatterns = [
    path('', include(router.urls)),
]
