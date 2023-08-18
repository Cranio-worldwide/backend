import base64

from django.core.files.base import ContentFile
from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import (Address, Currency, Language, Specialist,
                     SpecialistProfile, Specialization, SpecSpecialization, SpecLanguage)


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for model Address."""
    class Meta:
        fields = ('id', 'loc_latitude', 'loc_longitude', 'description',
                  'min_price', 'currency')
        model = Address
        validators = [UniqueTogetherValidator(
            queryset=Address.objects.all(),
            fields=('loc_latitude', 'loc_longitude', 'description'),
            message=_('You have already added this address')
        )]


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for model Currency."""
    class Meta:
        fields = ('id', 'slug', 'name')
        model = Currency


class Base64ImageField(serializers.ImageField):
    """Custom serializer field for User's photo."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ShortProfileSerializer(serializers.ModelSerializer):
    """Serializer for Specialist Profile - for search page."""
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    photo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = ('first_name', 'last_name', 'photo')
        model = SpecialistProfile


class FullProfileSerializer(ShortProfileSerializer):
    """Serializer for Specialist Profile - for details page."""
    about = serializers.CharField(required=False)
    diploma_issuer = serializers.CharField(required=False)
    diploma_recipient = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    practice_start = serializers.IntegerField(required=False)

    class Meta(ShortProfileSerializer.Meta):
        fields = ShortProfileSerializer.Meta.fields + (
            'about', 'diploma_issuer', 'diploma_recipient',
            'phone', 'practice_start',
        )

    def validate_phone(self, value):
        spec_id = self.context['spec_id']
        if (self.context['request'].method == 'PATCH' and Specialist.objects.
                filter(profile__phone=value).
                exclude(id=spec_id).
                exists()):
            raise serializers.ValidationError(_('Existing phone number.'))


class FullSpecialistSerializer(serializers.ModelSerializer):
    """Serializer for model Specialists - for details page."""
    profile = FullProfileSerializer(read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'email', 'profile', 'addresses')
        model = Specialist


class ShortSpecialistSerializer(serializers.ModelSerializer):
    """Serializer for model Specialists - for search page."""
    profile = ShortProfileSerializer(read_only=True)

    class Meta:
        fields = ('id', 'email', 'profile')
        model = Specialist


class SearchSerializer(serializers.ModelSerializer):
    """Serializer for search of specialists nearby."""
    specialist = ShortSpecialistSerializer(read_only=True)
    distance = serializers.DecimalField(max_digits=4, decimal_places=1,
                                        read_only=True)

    class Meta:
        fields = ('loc_latitude', 'loc_longitude', 'description', 'distance',
                  'min_price', 'currency', 'specialist')
        model = Address


class MeSpecialistSerializer(FullSpecialistSerializer):
    """Specialist serializer for Personal Area - /me endpoint."""
    status = serializers.SerializerMethodField()
    approver_comments = serializers.CharField(
        source='status.approver_comments')

    class Meta(FullSpecialistSerializer.Meta):
        fields = FullSpecialistSerializer.Meta.fields + (
            'status', 'approver_comments')

    def get_status(self, obj):
        return obj.status.get_stage_display()


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for list of available Languages."""
    class Meta:
        fields = ('id', 'title')
        model = Language


class SpecLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('language')
        model = SpecLanguage

    # @atomic
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     lang_id = validated_data.get('title')
    #     specialization, _ = Specialization.objects.get_or_create(title=lang_id)
    #     SpecSpecialization.objects.create(specialist=user, specialization=specialization)
    #     return super().create(validated_data)

    @atomic
    def create(self, validated_data):
        spoken_langs = []
        for data_set in validated_data:
            spec_id = data_set.get('specialist_id')
            lang_id = data_set.get('language')
            spoken_langs.append(SpecLanguage(specialist=spec_id, language=lang_id))
        SpecLanguage.objects.bulk_create(spoken_langs)
        return super().create(validated_data)


class SpecializationSerializer(serializers.ModelSerializer):
    """Serializer for list of available Languages."""
    class Meta:
        fields = ('id', 'title')
        model = Specialization


class SpecSpecializationSerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        fields = ('title')
        model = SpecSpecialization

    def validate(self, data):
        specialist = self.context['request'].user
        spec_title = data.get('title').capitalize()
        if specialist.specializations.filter(title=spec_title).exists():
            raise serializers.ValidationError(
                _('This specialization has already been added.')
            )
        return data

    @atomic
    def create(self, validated_data):
        user = self.context['request'].user
        spec_title = validated_data.get('title').capitalize()
        specialization, _ = Specialization.objects.get_or_create(title=spec_title)
        SpecSpecialization.objects.create(specialist=user, specialization=specialization)
        return super().create(validated_data)
