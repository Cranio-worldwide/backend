from django_filters import rest_framework as filters

from apps.api.models import StaticContent


class StaticContentFilter(filters.FilterSet):
    """Filter for static content via 'name' field"""
    class Meta:
        model = StaticContent
        fields = ('name',)

    def filter_queryset(self, queryset):
        name_filter = self.form.cleaned_data.get('name')
        if name_filter:
            values = name_filter.split(',')
            return queryset.filter(name__in=values)
        return queryset
