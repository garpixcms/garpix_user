from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from garpix_utils.string import get_random_string
from rest_framework import serializers

from garpix_user.mixins.serializers import PasswordSerializerMixin
from garpix_user.models.user_session import UserSession
from django.utils.translation import ugettext as _

User = get_user_model()


class RegistrationSerializer(PasswordSerializerMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)

    def validate_password_2(self, value):

        # check for password == password_2
        if value != self.initial_data.get('password'):
            raise serializers.ValidationError(_("Passwords do not match"))

        return value

    def validate_password(self, value):

        self._validate_password(value)

        return value

    def validate_email(self, value):

        GARPIX_USER_SETTINGS = settings.GARPIX_USER

        request = self.context.get('request')

        value = str(value).lower() if value else None

        queryset = User.objects.filter(email=value).first()
        if queryset is not None:
            raise serializers.ValidationError(_("This email is already in use"))

        if GARPIX_USER_SETTINGS.get('USE_PREREGISTRATION_EMAIL_CONFIRMATION', False) and GARPIX_USER_SETTINGS.get(
                'USE_EMAIL_CONFIRMATION', False):
            user = UserSession.get_or_create_user_session(request)
            if not user.is_email_confirmed:
                raise serializers.ValidationError(_('Email was not confirmed'))

        return value

    def validate_phone(self, value):

        GARPIX_USER_SETTINGS = settings.GARPIX_USER

        request = self.context.get('request')

        queryset = User.objects.filter(phone=value).first()
        if queryset is not None:
            raise serializers.ValidationError(_("This phone is already in use"))

        if GARPIX_USER_SETTINGS.get('USE_PREREGISTRATION_PHONE_CONFIRMATION', False) and GARPIX_USER_SETTINGS.get(
                'USE_PHONE_CONFIRMATION', False):
            user = UserSession.get_or_create_user_session(request)
            if not user.is_phone_confirmed:
                raise serializers.ValidationError(_('Phone number was not confirmed'))

        return value

    def create(self, validated_data):

        GARPIX_USER_SETTINGS = settings.GARPIX_USER

        request = self.context.get('request', None)

        validated_data.pop('password_2')

        user_data = validated_data

        if 'username' not in User.USERNAME_FIELDS and 'username' not in validated_data.keys():
            user_data.update({'username': get_random_string(25)})

        if GARPIX_USER_SETTINGS.get('USE_PHONE_CONFIRMATION', False) and not GARPIX_USER_SETTINGS.get('USE_PREREGISTRATION_PHONE_CONFIRMATION', False):
            user_data.update({'is_phone_confirmed': False})

        if GARPIX_USER_SETTINGS.get('USE_EMAIL_CONFIRMATION', False) and not GARPIX_USER_SETTINGS.get('USE_PREREGISTRATION_EMAIL_CONFIRMATION', False):
            user_data.update({'is_email_confirmed': False})

        with transaction.atomic():
            user = User.objects.create_user(**user_data)
            if request:
                user_session = UserSession.get_or_create_user_session(request)
                user_session.user = user
                user_session.recognized = UserSession.UserState.REGISTERED
                user_session.save()

        return user

    class Meta:
        model = User
        fields = ('password', 'password_2',)

    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)

        if getattr(User, 'USERNAME_FIELDS', None):
            return expanded_fields + User.USERNAME_FIELDS
        else:
            return expanded_fields

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        if USERNAME_FIELDS := getattr(User, 'USERNAME_FIELDS', None):
            for field in USERNAME_FIELDS:
                extra_kwargs.update({field: {'required': True, 'allow_blank': False}})

        return extra_kwargs
