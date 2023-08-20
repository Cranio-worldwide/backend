from django_filters import rest_framework as filters

from .models import Language, Specialization


class TitleAbstractFilter(filters.FilterSet):
    """Abstract class for icontains lookups in titles."""
    title = filters.CharFilter(lookup_expr='icontains')


class LanguageFilter(TitleAbstractFilter):
    class Meta:
        model = Language
        fields = ('title',)


class SpecializationFilter(TitleAbstractFilter):
    class Meta:
        model = Specialization
        fields = ('title',)
