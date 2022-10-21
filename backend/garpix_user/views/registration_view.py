from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView


from garpix_user.serializers import RegistrationSerializer
from garpix_user.utils.drf_spectacular import user_session_token_header_parameter

User = get_user_model()


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


registration_view = RegistrationView.as_view()
