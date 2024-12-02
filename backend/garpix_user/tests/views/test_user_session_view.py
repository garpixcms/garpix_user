from urllib.parse import urlencode
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ...models.user_session import UserSession

User = get_user_model()


class UserSessionViewTest(APITestCase):
    def test_create_user_session_guest(self):
        response = self.client.post(
            '/api/garpix_user/user_session/create_user_session/',
        )
        data = response.json()
        user_session = UserSession.objects.filter(recognized=UserSession.UserState.GUEST).first()

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {
            'session_user': {'token_number': user_session.token_number},
        })

    def test_create_user_session_authenticated(self):
        user = User.objects.create_user(username='test', password='test')
        self.client.force_authenticate(user)

        response = self.client.post(
            '/api/garpix_user/user_session/create_user_session/',
        )
        data = response.json()
        user_session = UserSession.objects.filter(recognized=UserSession.UserState.REGISTERED, user=user).first()

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {
            'session_user': {'token_number': user_session.token_number},
        })

    def test_create_user_session_existing_authenticated(self):
        user = User.objects.create_user(username='test', password='test')
        user_session = UserSession.objects.create(recognized=UserSession.UserState.GUEST, user=user, token_number='test')
        self.client.force_authenticate(user)

        response = self.client.post(
            '/api/garpix_user/user_session/create_user_session/',
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {
            'session_user': {'token_number': user_session.token_number},
        })

    def test_create_user_session_existing_from_header(self):
        user_session = UserSession.objects.create(recognized=UserSession.UserState.GUEST, token_number='test')

        response = self.client.post(
            '/api/garpix_user/user_session/create_user_session/',
            headers={
                UserSession.HEAD_NAME: user_session.token_number,
            }
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {
            'session_user': {'token_number': user_session.token_number},
        })

    def test_create_user_session_from_header(self):
        response = self.client.post(
            '/api/garpix_user/user_session/create_user_session/',
            headers={
                UserSession.HEAD_NAME: 'test',
            }
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {
            'session_user': {'token_number': 'test'},
        })
        self.assertTrue(UserSession.objects.filter(recognized=UserSession.UserState.UNRECOGNIZED, token_number='test').exists())

    def test_create_user_session_existing_from_session(self):
        UserSession.objects.create(recognized=UserSession.UserState.GUEST, token_number=self.client.session.session_key)

        response = self.client.post(
            '/api/garpix_user/user_session/create_user_session/',
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {
            'session_user': {'token_number': self.client.session.session_key},
        })
        self.assertEqual(1, UserSession.objects.count())

    def test_create_user_session_existing_from_username(self):
        user = User.objects.create_user(username='test', password='test')
        user_session = UserSession.objects.create(recognized=UserSession.UserState.GUEST, user=user, token_number='test')

        response = self.client.post(
            '/api/garpix_user/user_session/create_user_session/',
            QUERY_STRING=urlencode({'username': 'TeSt'}, doseq=True)
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(data, {
            'session_user': {'token_number': user_session.token_number},
        })
        self.assertEqual(1, UserSession.objects.count())
