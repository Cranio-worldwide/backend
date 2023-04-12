from django_filters import rest_framework as filters

from api.models import StaticContent


class StaticContentFilter(filters.FilterSet):
    """Filter for static content via 'name' field"""
    class Meta:
        model = StaticContent
        fields = ('name',)

    def filter_queryset(self, queryset):
        filter = self.form.cleaned_data.get('name')
        if filter:
            values = filter.split(',')
            queryset = queryset.filter(name__in=values)
        return queryset
