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
    specializations = serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = ('id', 'about', 'speciality', 'languages',
                  'specializations', 'service_types')
        model = Specialist
        read_only_fields = ('id',)

    def to_representation(self, instance):
        rep = OrderedDict()
        rep['id'] = instance.id
        rep['about'] = instance.about
        rep['speciality'] = instance.speciality
        rep['languages'] = LanguageSerializer(instance.languages, many=True).data
        rep['specializations'] = SpecializationSerializer(instance.specializations, many=True).data
        rep['service_types'] = ServiceTypeSerializer(instance.service_types, many=True).data
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
            capitalized_specs = list(map(lambda x: x[0].upper() + x[1:], specs))
            existing_specs = list(Specialization.objects.filter(title__in=capitalized_specs))
            if len(capitalized_specs) != len(existing_specs):
                db_titles = Specialization.objects.values_list('title', flat=True)
                new_specs = [Specialization(title=title) for title in capitalized_specs if title not in db_titles]
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
    photo = serializers.ReadOnlyField(source='user.photo')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    middle_name = serializers.ReadOnlyField(source='user.middle_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        fields = ('first_name', 'middle_name', 'last_name', 'photo')
        model = Specialist


# class FullSpecialistSerializer(SpecialistSerializer):
#     photo = serializers.ReadOnlyField(source='user.photo')
#     first_name = serializers.ReadOnlyField(source='user.first_name')
#     middle_name = serializers.ReadOnlyField(source='user.middle_name')
#     last_name = serializers.ReadOnlyField(source='user.last_name')
#     phone = serializers.ReadOnlyField(source='user.phone')

#     class Meta(SpecialistSerializer.Meta):
#         fields = SpecialistSerializer.Meta.fields + ('photo', 'first_name', 'middle_name', 'last_name', 'phone')


class SearchSerializer(serializers.ModelSerializer):
    """Serializer for search of specialists nearby."""
    specialist = ShortProfileSerializer(read_only=True)
    distance = serializers.DecimalField(max_digits=4, decimal_places=1,
                                        read_only=True)

    class Meta:
        fields = ('loc_latitude', 'loc_longitude', 'description', 'distance',
                  'min_price', 'currency', 'specialist')
        model = Address





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












# class ShortProfileSerializer(serializers.ModelSerializer):
#     """Serializer for Specialist Profile - for search page."""
#     first_name = serializers.CharField(required=False)
#     last_name = serializers.CharField(required=False)
#     photo = Base64ImageField(required=False, allow_null=True)

#     class Meta:
#         fields = ('first_name', 'last_name', 'photo')
#         model = Specialist


# class FullProfileSerializer(ShortProfileSerializer):
#     """Serializer for Specialist Profile - for details page."""
#     about = serializers.CharField(required=False)
#     diploma_issuer = serializers.CharField(required=False)
#     diploma_recipient = serializers.CharField(required=False)
#     phone = serializers.CharField(required=False)
#     practice_start = serializers.IntegerField(required=False)

#     class Meta(ShortProfileSerializer.Meta):
#         fields = ShortProfileSerializer.Meta.fields + (
#             'about', 'diploma_issuer', 'diploma_recipient',
#             'phone', 'practice_start',
#         )

#     def validate_phone(self, value):
#         spec_id = self.context['spec_id']
#         if (self.context['request'].method == 'PATCH' and Specialist.objects.
#                 filter(profile__phone=value).
#                 exclude(id=spec_id).
#                 exists()):
#             raise serializers.ValidationError(_('Existing phone number.'))


# class FullSpecialistSerializer(serializers.ModelSerializer):
#     """Serializer for model Specialists - for details page."""
#     profile = FullProfileSerializer(read_only=True)
#     addresses = AddressSerializer(many=True, read_only=True)

#     class Meta:
#         fields = ('id', 'email', 'profile', 'addresses')
#         model = Specialist


# class ShortSpecialistSerializer(serializers.ModelSerializer):
#     """Serializer for model Specialists - for search page."""
#     profile = ShortProfileSerializer(read_only=True)

#     class Meta:
#         fields = ('id', 'email', 'profile')
#         model = Specialist










# class SpecLanguageSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ('language')
#         model = SpecLanguage

    # @atomic
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     lang_id = validated_data.get('title')
    #     specialization, _ = Specialization.objects.get_or_create(title=lang_id)
    #     SpecSpecialization.objects.create(specialist=user, specialization=specialization)
    #     return super().create(validated_data)

    # @atomic
    # def create(self, validated_data):
    #     spoken_langs = []
    #     for data_set in validated_data:
    #         spec_id = data_set.get('specialist_id')
    #         lang_id = data_set.get('language')
    #         spoken_langs.append(SpecLanguage(specialist=spec_id, language=lang_id))
    #     SpecLanguage.objects.bulk_create(spoken_langs)
    #     return super().create(validated_data)





# class SpecSpecializationSerializer(serializers.ModelSerializer):
#     title = serializers.CharField()

#     class Meta:
#         fields = ('title')
#         model = SpecSpecialization

#     def validate(self, data):
#         specialist = self.context['request'].user
#         spec_title = data.get('title').capitalize()
#         if specialist.specializations.filter(title=spec_title).exists():
#             raise serializers.ValidationError(
#                 _('This specialization has already been added.')
#             )
#         return data

#     @atomic
#     def create(self, validated_data):
#         user = self.context['request'].user
#         spec_title = validated_data.get('title').capitalize()
#         specialization, _ = Specialization.objects.get_or_create(title=spec_title)
#         SpecSpecialization.objects.create(specialist=user, specialization=specialization)
#         return super().create(validated_data)
