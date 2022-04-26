from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from user.models import User

from garpix_auth.serializers import RegistrationSerializer


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer

