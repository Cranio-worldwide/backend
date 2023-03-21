from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

router = DefaultRouter()

router.register('v1/users', CustomUserViewSet, basename='customUser')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
