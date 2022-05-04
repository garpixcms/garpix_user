from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView


from garpix_auth.serializers import RegistrationSerializer


User = get_user_model()


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

