from django.db import IntegrityError
from django.utils.module_loading import import_string
from drf_spectacular.utils import extend_schema
from rest_framework import parsers, renderers
from rest_framework.fields import DateTimeField

from garpix_user.models.access_token import AccessToken as Token
from garpix_user.serializers.auth_token_serializer import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from garpix_user.models.refresh_token import RefreshToken
from garpix_user.utils.current_date import set_current_date
from garpix_user.utils.drf_spectacular import user_session_token_header_parameter
from django.utils.translation import gettext as _
import jwt


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def _get_access_token_data(self, user):
        token = Token.objects.create(user=user)
        refresh_token = RefreshToken.objects.create(user=user)
        return Response({
            'access_token': token.key,
            'refresh_token': refresh_token.key,
            'token_type': 'Bearer',
            'access_token_expires': settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS,
            'refresh_token_expires': settings.GARPIX_REFRESH_TOKEN_TTL_SECONDS,
        })

    def _get_jwt_data(self, user):
        jwt_secret_key = settings.GARPIX_USER.get('JWT_SECRET_KEY', None)

        if jwt_secret_key is None:
            raise IntegrityError(_('JWT_SECRET_KEY is not set'))

        serializer = import_string(
            settings.GARPIX_USER.get('JWT_SERIALIZER', 'garpix_user.serializers.JWTDataSerializer'))

        token = jwt.encode(
            {
                'created_at': DateTimeField().to_representation(set_current_date()),
                'username': user.username,
                'user_data': serializer(user).data
            },
            jwt_secret_key,
            algorithm='HS256'
        )

        return Response({
            'access_token': token,
            'token_type': 'Bearer',
            'access_token_expires': settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS
        })

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
