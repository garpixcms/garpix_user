from model_bakery import baker
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework.request import HttpRequest

from garpix_user.utils.backends import CustomAuthenticationBackend
from user.models import User


class CustomAuthenticationBackendTest(APITestCase):
    def setUp(self) -> None:
        self.auth = CustomAuthenticationBackend()

        self._all_users_delete()
        self.users = [
            ("test_user", self._create_user(username="test_user")),
            ("89009009090", self._create_user(phone="89009009090")),
            ("test@test.com", self._create_user(email="test@test.com")),
        ]

    def test_authenticate_none_credentials(self) -> None:
        response = self.auth.authenticate(HttpRequest(), username=None, password=None)
        self.assertIsNone(response)

        response = self.auth.authenticate(HttpRequest(), username="test", password=None)
        self.assertIsNone(response)

        response = self.auth.authenticate(HttpRequest(), username=None, password="test")
        self.assertIsNone(response)
    
    def test_authenticate_success(self) -> None:
        for username, user in self.users:
            self.assertEqual(user.login_attempts_count, 1)

            response_user = self.auth.authenticate(
                HttpRequest(),
                username=username,
                password="test_password",
            )
            user.refresh_from_db()

            self.assertEqual(response_user.pk, user.pk)
            self.assertEqual(response_user.login_attempts_count, user.login_attempts_count, 0)

    def test_authenticate_unsuccess(self) -> None:
        username, user = self.users[0]
        self.assertEqual(user.login_attempts_count, 1)

        response = self.auth.authenticate(HttpRequest(), username=username, password="invalid_password")
        self.assertIsNone(response)

        user.refresh_from_db()
        self.assertEqual(user.login_attempts_count, 2)
        self.assertFalse(user.is_blocked)

        settings.GARPIX_USER["ADMIN_PASSWORD_SETTINGS"] = False
        settings.GARPIX_USER["AVAILABLE_ATTEMPT"] = 3
        response = self.auth.authenticate(HttpRequest(), username=username, password="invalid_password")
        self.assertIsNone(response)

        user.refresh_from_db()
        self.assertEqual(user.login_attempts_count, 3)
        self.assertTrue(user.is_blocked)

        response = self.auth.authenticate(HttpRequest(), username="unknown", password="invalid_password")
        self.assertIsNone(response)

    def test_get_user(self) -> None:
        user = self.auth.get_user(self.users[0][1].pk)
        self.assertEqual(user.pk, self.users[0][1].pk)

    def test_get_user_does_not_exists(self) -> None:
        pk = max([user[1].pk for user in self.users]) + 1
        self.assertIsNone(self.auth.get_user(pk))
    
    def _create_user(self, attempts: int=1, **kwargs) -> User:
        user = baker.make(
            User,
            login_attempts_count=attempts,
            **kwargs,
        )
        user.set_password("test_password")
        return user

    def _all_users_delete(self) -> None:
        User.objects.all().delete()
