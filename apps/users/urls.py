from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VerifyEmail, UserViewSet


router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path('auth/verify-email/<uid>/<token>/', VerifyEmail.as_view()),
    path('auth/', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
