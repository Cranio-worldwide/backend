from rest_framework import serializers

from users.models import Specialists
from .models import Address, Services


class SpecialistsSerializer(serializers.ModelSerializer):
    """Serializer for model Specialists."""
    address = serializers.StringRelatedField(many=True, read_only=True)
    service = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'email', 'photo',
            'about', 'phone', 'experience', 'diploma', 'address', 'service'
        )
        model = Specialists


class AdressSerializers(serializers.ModelSerializer):
    """Serializer for model Address."""
    class Meta:
        fields = (
            'specialists_id', 'loc_latitude', 'loc_longitude', 'description'
        )
        model = Address


class ServicesSerializers(serializers.ModelSerializer):
    """Serializer for model Service."""
    class Meta:
        fields = (
            'specialists_id', 'name_service', 'price', 'currency',
            'description'
        )
        model = Services
