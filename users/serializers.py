from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """DoctorUser model serializer for admin."""
    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'email')
        model = CustomUser
