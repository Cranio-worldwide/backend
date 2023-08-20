import base64
from collections import OrderedDict

from django.core.files.base import ContentFile
from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.core.consts import ACCEPTABLE_FILES, FILE_SIZE_LIMIT

from .models import (Address, CranioDiploma, CranioInstitute, Currency,
                     Document, Language, ServiceType, Specialist,
                     Specialization, Status)


class DocumentSerializer(serializers.ModelSerializer):
    """Serializer for Specialist Documents."""
    class Meta:
        fields = ('id', 'file')
        model = Document

    def validate(self, data):
        file = data.get('file')
        type, extension = file.content_type.split('/')
        if extension not in ACCEPTABLE_FILES:
            raise serializers.ValidationError(
                _('This file type is not supported.')
            )
        if file.size > FILE_SIZE_LIMIT:
            raise serializers.ValidationError(
                _('Max acceptable file size is 5 megabytes.')
            )
        print(data)
        return data


class CranioInstituteSerializer(serializers.ModelSerializer):
    """Serializer for list of available Cranio Institute organizations."""
    class Meta:
        fields = ('id', 'title')
        model = CranioInstitute


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for list of available Languages."""
    class Meta:
        fields = ('id', 'title')
        model = Language


class SpecializationSerializer(serializers.ModelSerializer):
    """Serializer for list of available Specializations."""
    class Meta:
        fields = ('id', 'title')
        model = Specialization


class ServiceTypeSerializer(serializers.ModelSerializer):
    """Serializer for list of available Types of service."""
    class Meta:
        fields = ('id', 'title')
        model = ServiceType


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for model Currency."""
    class Meta:
        fields = ('id', 'slug', 'name')
        model = Currency


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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['currency'] = CurrencySerializer(instance.currency).data
        return rep


class Base64ImageField(serializers.ImageField):
    """Custom serializer field for User's photo."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class SpecialistSerializer(serializers.ModelSerializer):
    """Serializer for Specialists: personal are + profile page."""
    specializations = serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = ('id', 'about', 'phone', 'photo', 'speciality',
                  'first_name', 'middle_name', 'last_name',
                  'languages', 'specializations', 'service_types')
        model = Specialist
        read_only_fields = ('id',)

    def _get_photo_url(self, photo):
        request = self.context.get('request')
        return request.build_absolute_uri(photo.url)

    def to_representation(self, instance):
        rep = OrderedDict()
        rep['id'] = instance.id
        rep['about'] = instance.about
        rep['speciality'] = instance.speciality
        rep['languages'] = LanguageSerializer(
            instance.languages, many=True).data
        rep['specializations'] = SpecializationSerializer(
            instance.specializations, many=True).data
        rep['service_types'] = ServiceTypeSerializer(
            instance.service_types, many=True).data
        rep['first_name'] = instance.user.first_name
        rep['middle_name'] = instance.user.middle_name
        rep['last_name'] = instance.user.last_name
        rep['phone'] = instance.user.phone
        rep['photo'] = self._get_photo_url(instance.user.photo)
        return rep

    def _set_attrs(self, profile, services, langs, specs):
        if services is not None:
            profile.service_types.clear()
            profile.service_types.set(services)

        if langs is not None:
            profile.languages.clear()
            profile.languages.set(langs)

        if specs is not None:
            profile.specializations.clear()
            titled_specs = list(map(lambda x: x[0].upper() + x[1:], specs))
            existing_specs = list(Specialization.objects.filter(
                title__in=titled_specs
            ))
            if len(titled_specs) != len(existing_specs):
                db_titles = Specialization.objects.values_list('title',
                                                               flat=True)
                new_specs = [Specialization(title=title) for title
                             in titled_specs if title not in db_titles]
                new_specs = Specialization.objects.bulk_create(new_specs)
                existing_specs.extend(new_specs)

            profile.specializations.set(existing_specs)
        return profile

    @atomic
    def create(self, validated_data):
        services = validated_data.pop('service_types', None)
        langs = validated_data.pop('languages', None)
        specs = validated_data.pop('specializations', None)
        profile = Specialist.objects.create(**validated_data)
        self._set_attrs(profile, services, langs, specs)
        return profile

    @atomic
    def update(self, instance, validated_data):
        services = validated_data.pop('service_types', None)
        langs = validated_data.pop('languages', None)
        specs = validated_data.pop('specializations', None)
        self._set_attrs(instance, services, langs, specs)
        return super().update(instance, validated_data)


class CranioDiplomaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'organization', 'year', 'file')
        model = CranioDiploma
        read_only_fields = ('id',)

    def validate(self, data):
        user = self.context.get('request').user
        if hasattr(user, 'profile') and user.profile.status.stage not in [
                    Status.Stage.FILLING, Status.Stage.CHECK, Status.Stage.EDIT
                ]:
            raise serializers.ValidationError(
                _('Diploma data is not editable after verification.')
            )
        if not user.first_name or not user.last_name:
            raise serializers.ValidationError(
                _('Please fill in your first and last names.')
            )
        return data

    @atomic
    def create(self, validated_data):
        user = self.context.get('request').user
        specialist, created = Specialist.objects.get_or_create(user=user)
        if created:
            diploma = CranioDiploma.objects.create(
                specialist=specialist, **validated_data
            )
        else:
            diploma = specialist.diploma
            for attr, value in validated_data.items():
                setattr(diploma, attr, value)
            diploma.save()

        status, created_status = Status.objects.get_or_create(
            specialist=specialist, defaults={'stage': Status.Stage.CHECK}
        )
        if not created_status:
            status.stage = Status.Stage.CHECK
            status.save()

        # разбить на 3 функции-сервиса: спец, диплом, статус + уведомление
        return diploma


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'stage', 'comments', 'modified')
        model = Status

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['stage'] = instance.get_stage_display()
        return rep


class ShortProfileSerializer(serializers.ModelSerializer):
    """Serializer for Specialist Profile - for search page."""
    photo = serializers.ImageField(source='user.photo')
    first_name = serializers.CharField(source='user.first_name')
    middle_name = serializers.CharField(source='user.middle_name')
    last_name = serializers.CharField(source='user.last_name')
    phone = serializers.CharField(source='user.phone')

    class Meta:
        fields = ('speciality', 'photo', 'phone',
                  'first_name', 'middle_name', 'last_name')
        model = Specialist


class SearchSerializer(serializers.ModelSerializer):
    """Serializer for search of specialists nearby."""
    specialist = ShortProfileSerializer(read_only=True)
    distance = serializers.DecimalField(max_digits=4, decimal_places=1,
                                        read_only=True)

    class Meta:
        fields = ('loc_latitude', 'loc_longitude', 'description', 'distance',
                  'min_price', 'currency', 'specialist')
        model = Address
