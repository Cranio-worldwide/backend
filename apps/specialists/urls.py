from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, CurrencyViewSet, SearchList, SpecialistViewSet, LanguageViewSet, SpecializationViewSet

router = DefaultRouter()
router.register('specialists',
                SpecialistViewSet, basename='specialists')
router.register(r'specialists/(?P<specialist_id>[0-9a-f-]+)/addresses',
                AddressViewSet, basename='addresses')
# router.register(r'specialists/(?P<specialist_id>[0-9a-f-]+)/documents',
#                 AddressViewSet, basename='documents')
router.register('search', SearchList, basename='search')
router.register('currencies', CurrencyViewSet, basename='currencies')
router.register('languages', LanguageViewSet, basename='languages')
router.register('specializations',
                SpecializationViewSet, basename='specializations')


urlpatterns = [
    path('', include(router.urls)),
]
