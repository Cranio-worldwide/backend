from rest_framework import serializers

from .models import DoctorUser


class DoctorUserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели DoctorUser."""
    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'email',)
        model = DoctorUser
