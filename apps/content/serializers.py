from django.utils.translation import get_language_from_request
from rest_framework import serializers

from .models import AboutCranio, News, StaticContent


class NewsSerializer(serializers.ModelSerializer):
    """Serializer for model News."""
    class Meta:
        fields = ('id', 'date', 'picture', 'title', 'text')
        model = News


class StaticContentSerializer(serializers.ModelSerializer):
    """Serializer for model StaticContent."""
    static_fields = serializers.SerializerMethodField()

    class Meta:
        fields = ('name', 'static_fields')
        model = StaticContent
        lookup_field = 'name'

    def get_static_fields(self, obj):
        language = get_language_from_request(self.context['request'])
        field_name = f'fields_{language}'
        if hasattr(obj, field_name):
            return getattr(obj, field_name)
        return obj.fields_en


class AboutCranioSerializer(serializers.ModelSerializer):
    """Serializer for model AboutCranio - Main page."""
    class Meta:
        fields = ('id', 'text', 'image', 'link')
        model = AboutCranio
