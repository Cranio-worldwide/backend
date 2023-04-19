import datetime as dt
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import get_language_from_request
from rest_framework import serializers

from .models import Address, News, Service, StaticContent
from users.models import Specialist


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for model Address."""

    class Meta:
        fields = ('id', 'loc_latitude', 'loc_longitude', 'description')
        model = Address


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for model Service."""

    class Meta:
        fields = ('id', 'name_service', 'price', 'currency', 'description')
        model = Service


class SpecialistSerializer(serializers.ModelSerializer):
    """Serializer for model Specialists."""
    addresses = AddressSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    total_experience = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'email', 'photo', 'about',
            'phone', 'beginning_of_the_experience', 'total_experience',
            'diploma', 'addresses', 'services',
        )
        model = Specialist

    def get_total_experience(self, obj):
        return dt.datetime.now().year - obj.beginning_of_the_experience


class NewsSerializer(serializers.ModelSerializer):
    """Serializer for model News."""

    class Meta:
        fields = ('id', 'date', 'picture', 'description', 'published')
        model = News


class SpecialistCreateSerializer(serializers.ModelSerializer):
    """Serializer for users' authentification."""

    class Meta:
        model = Specialist
        fields = (
            'id', 'email', 'password',
            'first_name', 'last_name', 'photo',
            'about', 'phone', 'beginning_of_the_experience',
            'diploma', 'address', 'service'
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
        address = validated_data.pop('address')
        service = validated_data.pop('service')
        user = Specialist.objects.create(**validated_data)
        user.address.set(address)
        user.service.set(service)
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
        field_name = f'fields_{language}'
        if hasattr(obj, field_name):
            return getattr(obj, field_name)
        return obj.fields_en


class SearchSerializer(serializers.ModelSerializer):
    """Serializer for """
    specialist = SpecialistSerializer(read_only=True)
    distance = serializers.DecimalField(max_digits=4, decimal_places=1,
                                        read_only=True)
    min_price = serializers.IntegerField(read_only=True)
    max_price = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('loc_latitude', 'loc_longitude', 'min_price', 'max_price',
                  'distance', 'specialist')
        model = Address
