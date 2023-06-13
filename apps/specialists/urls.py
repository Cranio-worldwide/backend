from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (TokenObtainPairView,
#                                             TokenRefreshView)

from .views import (AddressViewSet, SpecialistViewSet, ServiceViewSet, SearchList)


router = DefaultRouter()
router.register('specialists', SpecialistViewSet, basename='specialists')
router.register(r'specialists/(?P<specialist_id>\d+)/addresses',
                AddressViewSet, basename='addresses')
router.register(r'specialists/(?P<specialist_id>\d+)/services',
                ServiceViewSet, basename='services')
router.register('search', SearchList, basename='search')


urlpatterns = [
    path('', include(router.urls)),
]
