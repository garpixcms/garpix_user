from django.conf import settings
from django.db import IntegrityError
from django.utils.module_loading import import_string
from rest_framework.fields import DateTimeField
from rest_framework.response import Response
from garpix_user.models.access_token import AccessToken as Token
from garpix_user.models.refresh_token import RefreshToken
from garpix_user.utils.current_date import set_current_date
from django.utils.translation import gettext as _
import jwt

from garpix_user.utils.get_password_settings import get_password_settings


class AuthTokenViewMixin:

    def _get_access_token_data(self, user):
        _password_settings = get_password_settings()

        token = Token.objects.create(user=user)
        refresh_token = RefreshToken.objects.create(user=user)
        return Response({
            'access_token': token.key,
            'refresh_token': refresh_token.key,
            'token_type': 'Bearer',
            'access_token_expires': _password_settings['access_token_ttl_seconds'],
            'refresh_token_expires': _password_settings['refresh_token_ttl_seconds'],
        })

    def _get_jwt_data(self, user):
        access_token_ttl_seconds = get_password_settings()['access_token_ttl_seconds']
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
            'access_token_expires': access_token_ttl_seconds
        })
