import jwt
from django.db import IntegrityError
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from garpix_user.utils.get_token_from_request import get_token_from_request
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext as _


def get_user_by_token(token):
    from ..models.access_token import AccessToken as Token
    from oauth2_provider.models import AccessToken
    User = get_user_model()

    # Refresh django rest token
    try:
        tok = Token.objects.get(key=token)
        if settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS > 0:
            if tok.created + timedelta(seconds=settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS) < timezone.now():
                tok.delete()
                raise Exception("Token expired.")
        user = User.active_objects.get(id=tok.user_id)
        return user
    except:  # noqa
        pass

    # Refresh social auth token
    try:
        tok = AccessToken.objects.get(token=token)
        if settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS > 0:
            if tok.created + timedelta(seconds=settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS) < timezone.now():
                tok.delete()
        else:
            user = tok.user
            return user
    except:  # noqa
        pass

    return AnonymousUser()


def get_user_by_jwt_token(token):
    User = get_user_model()

    jwt_secret_key = settings.GARPIX_USER.get('JWT_SECRET_KEY', None)

    if jwt_secret_key is None:
        raise IntegrityError(_('JWT_SECRET_KEY is not set'))

    try:
        token_data = jwt.decode(token, jwt_secret_key, algorithms='HS256', verify=True)

        if settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS > 0:
            if token_data['token_created_at'] + timedelta(
                    seconds=settings.GARPIX_ACCESS_TOKEN_TTL_SECONDS) < timezone.now():
                raise Exception("Token expired.")
        return User.active_objects.get(username=token_data['username'])
    except Exception as e:
        print(str(e))

    return AnonymousUser()


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

        if user is not None:
            return user, None
        return user, None
