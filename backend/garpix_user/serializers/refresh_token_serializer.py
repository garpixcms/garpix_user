from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(label=_("Refresh token"))
