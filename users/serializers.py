from rest_framework import serializers

from .models import DoctorUser


class DoctorUserSerializer(serializers.ModelSerializer):
    """DoctorUser model serializer for admin."""
    class Meta:
        fields = (
            'id', 'first_name', 'last_name', 'email')
        model = DoctorUser
