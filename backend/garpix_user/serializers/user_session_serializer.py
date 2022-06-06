from rest_framework.serializers import ModelSerializer

from ..models import UserSession


class UserSessionSerializer(ModelSerializer):
    class Meta:
        model = UserSession
        fields = (
            '__all__'
        )


class UserSessionTokenSerializer(ModelSerializer):
    class Meta:
        model = UserSession
        fields = ('token_number',)
