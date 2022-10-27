from django.contrib.auth import get_user_model

from garpix_user.serializers import RegistrationSerializer

User = get_user_model()


class RegistrationCustSerializer(RegistrationSerializer):

    class Meta(RegistrationSerializer.Meta):
        model = User
        fields = RegistrationSerializer.Meta.fields
