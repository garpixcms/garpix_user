from rest_framework import serializers

from garpix_user.mixins.serializers import ToLowerMixin, PasswordSerializerMixin
from django.utils.translation import gettext_lazy as _


class RestorePasswordSerializer(ToLowerMixin, serializers.Serializer):
    username = serializers.CharField(required=True, help_text=_('Email or phone number'))


class RestoreSetPasswordSerializer(PasswordSerializerMixin, serializers.Serializer):
    new_password = serializers.CharField(max_length=255, required=True)
    username = serializers.CharField(required=True, help_text=_('Email or phone number'))
    restore_password_confirm_code = serializers.CharField(max_length=15, required=True)

    def validate_new_password(self, value):
        self._validate_password(value)
        return value


class RestoreCheckCodeSerializer(serializers.Serializer):
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
