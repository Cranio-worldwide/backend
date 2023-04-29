import datetime as dt
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import get_language_from_request
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Address, News, Service, StaticContent
from users.models import Specialist


class SpecialistSerializer(serializers.ModelSerializer):
    """Serializer for model Specialists."""
    address = serializers.StringRelatedField(many=True, read_only=True)
    service = serializers.StringRelatedField(many=True, read_only=True)
    total_experience = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'email', 'photo',
            'about', 'phone', 'beginning_of_the_experience',
            'total_experience', 'diploma', 'address', 'service'
        )
        model = Specialist

    def get_total_experience(self, obj):
        return dt.datetime.now().year - obj.beginning_of_the_experience


class AdressSerializer(serializers.ModelSerializer):
    """Serializer for model Address."""

    class Meta:
        fields = (
            'specialists_id', 'loc_latitude', 'loc_longitude', 'description'
        )
        model = Address


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for model Service."""

    class Meta:
        fields = (
            'specialists_id', 'name_service', 'price', 'currency',
            'description'
        )
        model = Service


class NewsSerializer(serializers.ModelSerializer):
    """Serializer for model News."""
    class Meta:
        fields = ('id', 'date', 'picture', 'description', 'published')
        model = News


class SpecialistCreateSerializer(serializers.ModelSerializer):
    """Serializer for users' authentification."""
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=Specialist.objects.all())])
    photo = Base64ImageField(
        max_length=None,
        required=False,
        use_url=True)

    class Meta:
        model = Specialist
        fields = (
            'id', 'email', 'password',
            'first_name', 'last_name', 'photo',
            'about', 'phone', 'beginning_of_the_experience', 'diploma'
        )
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True,
                         'write_only': True},
        }

    def validate_password(self, data):
        try:
            validate_password(data)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Specialist.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class StaticContentSerializer(serializers.ModelSerializer):
    """Serializer for model StaticContent."""
    static_fields = serializers.SerializerMethodField()

    class Meta:
        fields = ('name', 'static_fields')
        model = StaticContent
        lookup_field = 'name'

    def get_static_fields(self, obj):
        language = get_language_from_request(self.context['request'])
        if language == 'en':
            return obj.fields_en
        return obj.fields_ru
