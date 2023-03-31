import datetime as dt

from rest_framework import serializers

from users.models import Specialist

from .models import Address, News, Service


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


# class CountrySerializer(serializers.ModelSerializer):
#     """Serializer for model Country."""
#     class Meta:
#         fields = ('id', 'name')
#         model = Country


# class CitySerializer(serializers.ModelSerializer):
#     """Serializer for model City."""
#     coordinates = serializers.SerializerMethodField()

#     class Meta:
#         fields = ('id', 'name', 'coordinates')
#         model = City

#     def get_coordinates(self, obj):
#         return f'{obj.latitude}, {obj.longitude}'


class NewsSerializer(serializers.ModelSerializer):
    """Serializer for model News."""
    class Meta:
        fields = ('id', 'date', 'picture', 'description', 'published')
        model = News
