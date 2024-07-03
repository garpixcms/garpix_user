import jwt
from django.db import IntegrityError
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

from garpix_user.utils.get_password_settings import get_password_settings
from garpix_user.utils.get_token_from_request import get_token_from_request
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext as _


User = get_user_model()


def check_token_lifetime(token, ttl):
    if ttl <= 0:
        return

    if token.created + timedelta(seconds=ttl) < timezone.now():
        token.delete()
        raise exceptions.AuthenticationFailed(_('Token expired.'))


def get_user_by_token_query(**kwargs):
    try:
        return User.active_objects.get(is_blocked=False, **kwargs)
    except User.DoesNotExist:
        raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))


def get_user_by_token(token):
    from ..models.access_token import AccessToken as Token
    from oauth2_provider.models import AccessToken

    access_token_ttl_seconds = get_password_settings()['access_token_ttl_seconds']

    # Refresh django rest token
    try:
        tok = Token.objects.get(key=token)
        check_token_lifetime(tok, access_token_ttl_seconds)

        return get_user_by_token_query(pk=tok.user_id)
    except Token.DoesNotExist:
        pass

    # Refresh social auth token
    try:
        tok = AccessToken.objects.get(token=token)
        check_token_lifetime(tok, access_token_ttl_seconds)

        return get_user_by_token_query(pk=tok.user_id)
    except AccessToken.DoesNotExist:
        pass

    raise exceptions.AuthenticationFailed(_('Invalid token.'))


def get_user_by_jwt_token(token):
    access_token_ttl_seconds = get_password_settings()['access_token_ttl_seconds']

    jwt_secret_key = settings.GARPIX_USER.get('JWT_SECRET_KEY', None)
    if jwt_secret_key is None:
        raise IntegrityError(_('JWT_SECRET_KEY is not set'))

    try:
        token_data = jwt.decode(token, jwt_secret_key, algorithms='HS256', verify=True)

        if access_token_ttl_seconds > 0:
            if token_data['token_created_at'] + timedelta(
                    seconds=access_token_ttl_seconds) < timezone.now():
                raise exceptions.AuthenticationFailed(_('Token expired.'))

        return get_user_by_token_query(username=token_data['username'])
    except jwt.DecodeError:
        raise exceptions.AuthenticationFailed(_('Invalid token.'))


class MainAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        token = get_token_from_request(request, keyword=self.keyword)
        if token is None:
            return None

        use_jwt = settings.GARPIX_USER.get('REST_AUTH_TOKEN_JWT', False)

        if use_jwt:
            user = get_user_by_jwt_token(token)
        else:
            user = get_user_by_token(token)

        return user, None
