from django.contrib.auth import get_user_model
from rest_framework import serializers

from garpix_user.serializers import RegistrationSerializer

User = get_user_model()


class RegistrationCustSerializer(RegistrationSerializer):
    # extra_field = serializers.CharField(write_only=True)

    class Meta(RegistrationSerializer.Meta):
        model = User
        fields = RegistrationSerializer.Meta.fields
