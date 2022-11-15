from drf_spectacular.utils import extend_schema
from rest_framework import parsers, renderers

from garpix_user.mixins.views import ActivateTranslationMixin
from garpix_user.models.access_token import AccessToken as Token
from garpix_user.serializers.auth_token_serializer import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from garpix_user.models.refresh_token import RefreshToken
from garpix_user.utils.drf_spectacular import user_session_token_header_parameter


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class ObtainAuthToken(ActivateTranslationMixin, APIView):
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
        token = Token.objects.create(user=user)
        refresh_token = RefreshToken.objects.create(user=user)
        return Response({
            'access_token': token.key,
            'refresh_token': refresh_token.key,
            'token_type': 'Bearer',
            'access_token_expires': settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS,
            'refresh_token_expires': settings.GARPIX_REFRESH_TOKEN_TTL_SECONDS,
        })


obtain_auth_token = ObtainAuthToken.as_view()
