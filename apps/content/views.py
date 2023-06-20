from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import StaticContentFilter
from .models import News, StaticContent
from .serializers import NewsSerializer, StaticContentSerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for model News. Adds/changes - through admin panel."""
    serializer_class = NewsSerializer
    queryset = News.objects.all()


class StaticContentViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for transfer of multilingual static content to frontend
       Filtering via 'name' parameter: use comma(',') for multiple filter
    """
    serializer_class = StaticContentSerializer
    queryset = StaticContent.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StaticContentFilter
    lookup_field = 'name'
