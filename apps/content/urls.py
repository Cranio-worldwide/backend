from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (NewsViewSet, StaticContentViewSet)


router = DefaultRouter()
router.register('news', NewsViewSet, basename='news'),
router.register('static', StaticContentViewSet, basename='static')


urlpatterns = [
    path('', include(router.urls)),
]
