from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'email', 'role')
        model = CustomUser
        read_only_fields = ('id', 'email', 'role')
