from rest_framework.serializers import ModelSerializer

from garpix_user.models.user_session import UserSession


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
