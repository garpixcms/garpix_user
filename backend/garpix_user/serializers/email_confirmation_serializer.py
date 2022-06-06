from garpix_user.mixins.serializers import ToLowerMixin


from rest_framework import serializers


class EmailPreConfirmSendSerializer(ToLowerMixin, serializers.Serializer):
    email = serializers.EmailField()


class EmailConfirmSendSerializer(ToLowerMixin, serializers.Serializer):
    email = serializers.EmailField(required=False)


class EmailConfirmCheckCodeSerializer(serializers.Serializer):
    email_confirmation_code = serializers.CharField(max_length=255)
