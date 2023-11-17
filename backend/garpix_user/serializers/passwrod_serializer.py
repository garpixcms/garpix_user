from rest_framework import serializers

from garpix_user.mixins.serializers import ToLowerMixin, PasswordSerializerMixin
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import authenticate


class RestorePasswordSerializer(ToLowerMixin, serializers.Serializer):
    username = serializers.CharField(required=True, help_text=_('Email or phone number'))


class RestoreSetPasswordSerializer(ToLowerMixin, PasswordSerializerMixin, serializers.Serializer):
    new_password = serializers.CharField(max_length=255, required=True)
    username = serializers.CharField(required=True, help_text=_('Email or phone number'))
    restore_password_confirm_code = serializers.CharField(max_length=15, required=True)

    def validate_new_password(self, value):
        self._validate_password(value)
        return value


class RestoreCheckCodeSerializer(ToLowerMixin, serializers.Serializer):
    restore_password_confirm_code = serializers.CharField(max_length=15, required=True)
    username = serializers.CharField(required=True, help_text=_('Email or phone number'))


class ChangePasswordSerializer(PasswordSerializerMixin, serializers.Serializer):
    new_password = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        self._validate_password(value)
        return value

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Password is incorrect')
            )
        return value


class ChangePasswordUnauthorizedSerializer(PasswordSerializerMixin, serializers.Serializer):
    username = serializers.CharField(label=_("Username"), required=True, write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=True,
        write_only=True
    )
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_2 = serializers.CharField(write_only=True, required=True)

    def validate_new_password(self, value):
        self._validate_password(value)
        return value

    def validate_new_password_2(self, value):

        if value != self.initial_data.get('new_password'):
            raise serializers.ValidationError(_("Passwords do not match"))

        return value

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        username = username.lower()
        request = self.context.get('request')

        user = authenticate(request=request,
                            username=username, password=password)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        if user.is_blocked:
            msg = _(
                'Your account is blocked. Please contact your administrator')
            raise serializers.ValidationError(msg, code='authorization')

        super().validate(attrs)

        attrs['user'] = user

        return attrs
