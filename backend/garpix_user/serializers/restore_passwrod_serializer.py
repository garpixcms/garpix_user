from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from garpix_user.mixins.serializers import ToLowerMixin


class RestorePasswordSerializer(ToLowerMixin, serializers.Serializer):
    username = serializers.CharField(required=True)


class RestoreByPhoneSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)


class RestoreSetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=255, required=True)


class RestoreCheckCodeSerializer(serializers.Serializer):
    restore_password_confirm_code = serializers.CharField(max_length=15, required=True)
