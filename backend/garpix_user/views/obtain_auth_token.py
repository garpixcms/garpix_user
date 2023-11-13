from drf_spectacular.utils import extend_schema
from rest_framework import parsers, renderers

from garpix_user.mixins.views.auth_token_mixin import AuthTokenViewMixin
from garpix_user.serializers.auth_token_serializer import AuthTokenSerializer
from rest_framework.views import APIView
from django.conf import settings
from garpix_user.utils.drf_spectacular import user_session_token_header_parameter


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class ObtainAuthToken(AuthTokenViewMixin, APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        use_jwt = settings.GARPIX_USER.get('REST_AUTH_TOKEN_JWT', False)

        if use_jwt:
            return self._get_jwt_data(user)
        return self._get_access_token_data(user)


obtain_auth_token = ObtainAuthToken.as_view()
