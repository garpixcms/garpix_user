from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from garpix_utils.string import get_random_string
from rest_framework import serializers

from garpix_user.models.user_session import UserSession
from django.utils.translation import ugettext as _

User = get_user_model()

GARPIX_USER_SETTINGS = settings.GARPIX_USER


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)

    def validate_password(self, value):

        min_length = GARPIX_USER_SETTINGS.get('MIN_LENGTH_PASSWORD', 8)
        min_digits = GARPIX_USER_SETTINGS.get('MIN_DIGITS_PASSWORD', 2)
        min_chars = GARPIX_USER_SETTINGS.get('MIN_CHARS_PASSWORD', 2)
        min_uppercase = GARPIX_USER_SETTINGS.get('MIN_UPPERCASE_PASSWORD', 1)

        # check for 2 min length
        if len(value) < min_length:
            raise serializers.ValidationError(
                _('Password must be at least {min_length} characters long.'.format(min_length=min_length))
            )

        # check for 2 digits
        if sum(c.isdigit() for c in value) < min_digits:
            raise serializers.ValidationError(
                _('Password must container at least {min_digits} digits.'.format(min_digits=min_digits))
            )

        # check for 2 char
        if sum(c.isalpha() for c in value) < min_chars:
            raise serializers.ValidationError(
                _('Password must container at least {min_chars} chars.'.format(min_chars=min_chars))
            )

        # check for uppercase letter
        if sum(c.isupper() for c in value) < min_uppercase:
            raise serializers.ValidationError(
                _('Password must container at least {min_uppercase} uppercase letter.'.format(
                    min_uppercase=min_uppercase))
            )

        # check for password = password_2
        if value != self.initial_data.get('password_2'):
            raise serializers.ValidationError(_("Passwords do not match"))

        return value

    def validate_email(self, value):

        request = self.context.get('request')

        queryset = User.objects.filter(email=value, is_email_confirmed=True).first()
        if queryset is not None:
            raise serializers.ValidationError(_("This email is already in use"))

        if GARPIX_USER_SETTINGS.get('USE_PREREGISTRATION_EMAIL_CONFIRMATION', False) and GARPIX_USER_SETTINGS.get(
                'USE_EMAIL_CONFIRMATION', False):
            user = UserSession.get_or_create_user_session(request)
            if not user.is_email_confirmed:
                raise serializers.ValidationError(_('Email was not confirmed'))

        return value

    def validate_phone(self, value):

        request = self.context.get('request')

        queryset = User.objects.filter(phone=value, is_phone_confirmed=True).first()
        if queryset is not None:
            raise serializers.ValidationError(_("This phone is already in use"))

        if GARPIX_USER_SETTINGS.get('USE_PREREGISTRATION_PHONE_CONFIRMATION', False) and GARPIX_USER_SETTINGS.get(
                'USE_PHONE_CONFIRMATION', False):
            user = UserSession.get_or_create_user_session(request)
            if not user.is_phone_confirmed:
                raise serializers.ValidationError(_('Phone number was not confirmed'))

        return value

    def create(self, validated_data):

        request = self.context.get('request', None)

        validated_data.pop('password_2')

        user_data = validated_data

        if 'username' not in validated_data.keys():
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
