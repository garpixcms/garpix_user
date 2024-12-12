import time
from datetime import timedelta

import jwt
from django.db import IntegrityError
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APITestCase
from rest_framework.request import HttpRequest
from model_bakery import baker
from oauth2_provider.models import AccessToken

from garpix_user.models.access_token import AccessToken as Token
from garpix_user.rest.authentication import (
    MainAuthentication,
    get_user_by_token,
    get_user_by_jwt_token,
)


class GetUserByToken(APITestCase):
    def setUp(self) -> None:
        self._delete_all_tokens()
        self._delete_all_users()
        self.user = baker.make(get_user_model(), username="test_user")
        self.token = baker.make(Token, key="token_key", user=self.user)
        self.oauth_token = baker.make(
            AccessToken,
            token="token_key",
            user=self.user,
            token_checksum="checksum",
        )

    def test_get_user_by_token(self) -> None:
        settings.GARPIX_USER["ADMIN_PASSWORD_SETTINGS"] = False
        settings.GARPIX_USER["ACCESS_TOKEN_TTL_SECONDS"] = 0
        user = get_user_by_token(self.token.key)
        self.assertEqual(user.id, self.user.id)

        user = get_user_by_token(self.oauth_token.token)
        self.assertEqual(user.id, self.user.id)

    def test_get_user_by_token_expired(self) -> None:
        settings.GARPIX_USER["ADMIN_PASSWORD_SETTINGS"] = False
        settings.GARPIX_USER["ACCESS_TOKEN_TTL_SECONDS"] = 1

        self.token.created -= timedelta(seconds=2)
        self.token.save()

        self.oauth_token.created -= timedelta(seconds=2)
        self.oauth_token.save()

        self.assertIsInstance(get_user_by_token(self.token.key), AnonymousUser)
        self.assertIsInstance(get_user_by_token(self.oauth_token.token), AnonymousUser)

    def _delete_all_tokens(self) -> None:
        Token.objects.all().delete()
        AccessToken.objects.all().delete()

    def _delete_all_users(self) -> None:
        get_user_model().objects.all().delete()


class GetUserByJWTToken(APITestCase):
    def setUp(self) -> None:
        settings.GARPIX_USER["ADMIN_PASSWORD_SETTINGS"] = False
        self._delete_all_users()
        self.user = baker.make(get_user_model(), username="test_user")

    def test_get_user_by_jwt_token_raise(self) -> None:
        settings.GARPIX_USER["JWT_SECRET_KEY"] = None
        with self.assertRaises(IntegrityError):
            get_user_by_jwt_token("token")

    def test_get_user_by_jwt_token(self) -> None:
        settings.GARPIX_USER["JWT_SECRET_KEY"] = "secret_key"
        settings.GARPIX_USER["ACCESS_TOKEN_TTL_SECONDS"] = 0
        token = jwt.encode({"username": self.user.username}, key="secret_key", algorithm="HS256")
        self.assertEqual(get_user_by_jwt_token(token).id, self.user.id)

    def test_get_user_by_jwt_anonymous(self) -> None:
        settings.GARPIX_USER["JWT_SECRET_KEY"] = "secret_key"
        settings.GARPIX_USER["ACCESS_TOKEN_TTL_SECONDS"] = 1

        token = jwt.encode(
            {
                "username": self.user.username,
                "token_created_at": str(timezone.now() - timedelta(seconds=2)),
            },
            key="secret_key",
            algorithm="HS256",
        )

        self.assertIsInstance(get_user_by_jwt_token(token), AnonymousUser)
    
    def _delete_all_users(self) -> None:
        get_user_model().objects.all().delete()


class MainAuthenticationTest(APITestCase):
    def setUp(self) -> None:
        self._delete_all_tokens()
        self._delete_all_users()
        self.auth = MainAuthentication()
        self.user = baker.make(get_user_model(), username="test_user")
        self.token = baker.make(Token, key="secret_key", user=self.user)
        self.jwt_token = jwt.encode({"username": self.user.username}, key="secret_key", algorithm="HS256")
        settings.GARPIX_USER["JWT_SECRET_KEY"] = "secret_key"
        settings.GARPIX_USER["REST_AUTH_HEADER_KEY"] = True
        del settings.GARPIX_USER["REST_AUTH_HEADER_KEY"]
        settings.GARPIX_USER["ADMIN_PASSWORD_SETTINGS"] = False
        settings.GARPIX_USER["ACCESS_TOKEN_TTL_SECONDS"] = 0

    def test_authenticate_token_does_not_exists(self) -> None:
        request = HttpRequest()
        self.assertIsNone(self.auth.authenticate(request))

    def test_authenticate_token_jwt(self) -> None:
        settings.GARPIX_USER["REST_AUTH_TOKEN_JWT"] = True
        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = f"Bearer {self.jwt_token}"
        self.assertEqual(self.auth.authenticate(request)[0].id, self.user.id)

    def test_authenticate_token(self) -> None:
        settings.GARPIX_USER["REST_AUTH_TOKEN_JWT"] = False
        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = "Bearer secret_key"
        self.assertEqual(self.auth.authenticate(request)[0].id, self.user.id)
 
    def _delete_all_tokens(self) -> None:
        Token.objects.all().delete()
        AccessToken.objects.all().delete()

    def _delete_all_users(self) -> None:
        get_user_model().objects.all().delete()
