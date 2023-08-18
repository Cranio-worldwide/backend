from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'email', 'is_specialist')
        model = CustomUser
        read_only_fields = ('id', 'email', 'is_specialist')
