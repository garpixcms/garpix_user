from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField as BasePhoneNumberField


class PhoneNumberField(BasePhoneNumberField):
    def run_validation(self, data=None):
        try:
            return super().run_validation(data)
        except ValidationError:
            raise ValidationError(_("Enter a valid phone number"))

class PhoneConfirmSendSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=False)


class PhonePreConfirmSendSerializer(serializers.Serializer):
    phone = PhoneNumberField()


class PhoneConfirmCheckCodeSerializer(serializers.Serializer):
    phone_confirmation_code = serializers.CharField(max_length=15)
