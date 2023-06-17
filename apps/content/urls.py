from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (NewsViewSet, GeopositionViewSet, StaticContentViewSet)


router = DefaultRouter()
router.register('news', NewsViewSet, basename='news'),
router.register('me', GeopositionViewSet, basename='me')
router.register('static', StaticContentViewSet, basename='static')


urlpatterns = [
    path('', include(router.urls)),
]
