from rest_framework import serializers

from .models import DoctorUser


class DoctorUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели DoctorUser."""
    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'email', 'photo', 'country',
            'city', 'street', 'building', 'office', 'about', 'price',
            'phone', 'experience'
        )
        model = DoctorUser
