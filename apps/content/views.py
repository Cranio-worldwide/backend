from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import StaticContentFilter
from .models import AboutCranio, News, StaticContent
from .serializers import (AboutCranioSerializer, NewsSerializer,
                          StaticContentSerializer)


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for model News. Adds/changes - through admin panel."""
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_published=True)
    pagination_class = LimitOffsetPagination


class StaticContentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for transfer of multilingual static content to frontend.
    Filtering via 'name' parameter: use comma(',') for multiple filter.
    """
    serializer_class = StaticContentSerializer
    queryset = StaticContent.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = StaticContentFilter
    lookup_field = 'name'


class AboutCranioView(views.APIView):
    """Static block with info about Craniosacral therapy."""
    def get(self, request):
        try:
            about = AboutCranio.objects.get(is_published=True)
        except ObjectDoesNotExist:
            return Response({"data": "no data yet"})
        serializer = AboutCranioSerializer(instance=about)
        return Response(serializer.data)
