from django.urls import reverse
from django.test import override_settings
import time

from garpix_user.tests.utils.test_case_mixin import ApiTestMixin
from django.utils.translation import ugettext_lazy as _


class LoginApiTest(ApiTestMixin):
    def setUp(self):
        self.set_init_data()

    def test_invalid_username_password(self):
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['username'],
                'password': 'passwordtest',
            },
            HTTP_ACCEPT='application/json'
        )

        self.assertDictEqual(response.json(), {"non_field_errors": [_("Unable to log in with provided credentials.")]})

    def test_valid_username_password(self):
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['username'],
                'password': self.user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

    def test_access_to_protected_view(self):
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json')
        self.assertDictEqual(response.json(), {'detail': _('Authentication credentials were not provided.')})
        # auth
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['username'],
                'password': self.user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token = response.json()['access_token']
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertDictEqual(response.json(), {'username': self.user_data['username']})

    def test_access_to_protected_view_after_logout(self):
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['username'],
                'password': self.user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token = response.json()['access_token']
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertDictEqual(response.json(), {'username': self.user_data['username']})
        # logout
        response = self.client.post(reverse('garpix_user:garpix_user_api:api_logout'), HTTP_ACCEPT='application/json',
                                    HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertDictEqual(response.json(), {'result': True})
        # get protected view after logout
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json')
        self.assertDictEqual(response.json(), {'detail': _('Authentication credentials were not provided.')})

    @override_settings(GARPIX_ACCESS_TOKEN_TTL_SECONDS=5)
    def test_refresh_token(self):
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['username'],
                'password': self.user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token1 = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token1}')
        self.assertDictEqual(response.json(), {'username': self.user_data['username']})
        # wait and get protected view with expired access token
        time.sleep(5)
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json')
        self.assertDictEqual(response.json(), {'detail': _('Authentication credentials were not provided.')})
        # refresh token
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_refresh'),
            {
                'refresh_token': refresh_token,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token2 = response.json()['access_token']
        self.assertNotEqual(access_token1, access_token2)
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token2}')
        self.assertDictEqual(response.json(), {'username': self.user_data['username']})

    @override_settings(GARPIX_REFRESH_TOKEN_TTL_SECONDS=5)
    def test_refresh_token_expired(self):
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['username'],
                'password': self.user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        # get protected view
        response = self.client.get(reverse('current-user'), HTTP_ACCEPT='application/json',
                                   HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertDictEqual(response.json(), {'username': self.user_data['username']})
        # refresh token
        time.sleep(5)
        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_refresh'),
            {
                'refresh_token': refresh_token,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'result': False})

    def test_login_by_email(self):
        self.User.USERNAME_FIELDS = ('email',)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['email'],
                'password': self.user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

    def test_login_by_phone(self):
        self.User.USERNAME_FIELDS = ('phone',)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['phone'],
                'password': self.user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

    def test_login_by_phone_or_email(self):
        self.User.USERNAME_FIELDS = ('phone', 'email')

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['phone'],
                'password': self.user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.user_data['email'],
                'password': self.user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)
