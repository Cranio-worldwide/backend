import base64
import datetime as dt
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.translation import get_language_from_request
from rest_framework import serializers

from .models import Address, Service, Specialist, SpecialistData


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


class Base64ImageField(serializers.ImageField):
    """Custom serializer field for User's photo."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ShortProfileSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('first_name', 'last_name', 'photo')
        model = SpecialistData


class FullProfileSerializer(ShortProfileSerializer):
    total_experience = serializers.SerializerMethodField()

    class Meta(ShortProfileSerializer.Meta):
        fields = ShortProfileSerializer.Meta.fields + (
            'about', 'diploma_issuer', 'diploma_recipient',
            'phone', 'practice_start', 'total_experience'
        )

    def get_total_experience(self, obj):
        if not obj.practice_start:
            return None
        return dt.datetime.now().year - obj.practice_start


class ShortSpecialistSerializer(serializers.ModelSerializer):
    """Serializer for model Specialists."""
    profile = ShortProfileSerializer(read_only=True, source='data')
    addresses = AddressSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'id', 'email', 'profile', 'addresses', 'services',
        )
        model = Specialist


class FullSpecialistSerializer(ShortSpecialistSerializer):
    """Serializer for model Specialists."""
    profile = FullProfileSerializer(read_only=True, source='data')



# class SpecialistCreateSerializer(serializers.ModelSerializer):
#     """Serializer for users' authentification."""

#     class Meta:
#         model = Specialist

#         fields = ('id', 'email', 'password',)

#         extra_kwargs = {
#             'email': {'required': True},
#             'password': {'required': True,
#                          'write_only': True},
#         }

#     def validate_password(self, data):
#         try:
#             validate_password(data)
#         except ValidationError as exc:
#             raise serializers.ValidationError(str(exc))
#         return data

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = Specialist.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user


class SearchSerializer(serializers.ModelSerializer):
    """Serializer for search of specialists nearby."""
    specialist = ShortSpecialistSerializer(read_only=True)
    distance = serializers.DecimalField(max_digits=4, decimal_places=1,
                                        read_only=True)
    min_price = serializers.IntegerField(read_only=True)
    max_price = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('loc_latitude', 'loc_longitude', 'min_price', 'max_price',
                  'distance', 'specialist')
        model = Address