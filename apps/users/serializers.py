import base64

from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import CustomUser


class Base64ImageField(serializers.ImageField):
    """Custom serializer field for User's photo."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('id', 'email', 'role',
                  'first_name', 'middle_name', 'last_name',
                  'phone', 'photo')
        model = CustomUser
        read_only_fields = ('id', 'email', 'role')


class CreateUserSerializer(serializers.ModelSerializer):
    """User registration serializer."""
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        value = value.lower()
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _('There is already a user with the same e-mail address.')
            )
        return value

    def create(self, validated_data: dict) -> CustomUser:
        return CustomUser.objects.create_user(**validated_data)


# class MeSpecialistSerializer(UserSerializer):
#     """Specialist serializer for Personal Area - /me endpoint."""
#     status = serializers.SerializerMethodField()
#     approver_comments = serializers.CharField(
#         source='status.approver_comments')

#     class Meta(UserSerializer.Meta):
#         fields = UserSerializer.Meta.fields + (
#             'status', 'approver_comments')

#     def get_status(self, obj):
#         return obj.status.get_stage_display()
