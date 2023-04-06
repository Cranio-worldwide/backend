from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (AdressViewSet, SpecialistViewSet, ServiceViewSet,
                    NewsViewSet, GeopositionViewSet, RegisterView, VerifyEmail)


router = DefaultRouter()

router.register('specialists', SpecialistViewSet, basename='specialists')
router.register('address', AdressViewSet, basename='address')
router.register('services', ServiceViewSet, basename='services')
# router.register('countries', CountryViewSet, basename='countries')
# router.register(r'countries/(?P<country_id>\d+)/cities', CityViewSet,
#                 basename='cities')
router.register('news', NewsViewSet, basename='news'),
router.register('me', GeopositionViewSet, basename='me')


auth_patterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='sign_up'),
    path('verify-email/', VerifyEmail.as_view(), name='verify_email'),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router.urls)),
]
