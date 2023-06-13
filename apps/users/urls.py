from django.urls import include, path
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (TokenObtainPairView,
#                                             TokenRefreshView)

# from .views import (AddressViewSet, SpecialistViewSet, ServiceViewSet,
#                     NewsViewSet, GeopositionViewSet, RegisterView, VerifyEmail,
#                     StaticContentViewSet, SearchList)


# router = DefaultRouter()


# auth_patterns = [
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('register/', RegisterView.as_view(), name='sign_up'),
#     path('verify-email/', VerifyEmail.as_view(), name='verify_email'),
# ]

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
