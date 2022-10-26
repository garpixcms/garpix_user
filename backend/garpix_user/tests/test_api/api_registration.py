from django.urls import reverse
from django.test import override_settings

from garpix_user.tests.utils.settings import GARPIX_USER_SETTINGS
from garpix_user.tests.utils.test_case_mixin import ApiTestMixin


class RegistrationApiTest(ApiTestMixin):
    def setUp(self):
        self.set_init_data()

    @override_settings(GARPIX_USER=GARPIX_USER_SETTINGS)
    def test_registration_by_email(self):
        self.User.USERNAME_FIELDS = ('email',)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'email': self.new_user_data['email'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.new_user_data['email'],
                'password': self.new_user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

    @override_settings(GARPIX_USER=GARPIX_USER_SETTINGS)
    def test_registration_by_phone(self):
        self.User.USERNAME_FIELDS = ('phone',)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.new_user_data['phone'],
                'password': self.new_user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

    @override_settings(GARPIX_USER=GARPIX_USER_SETTINGS)
    def test_registration_by_phone_or_email(self):
        self.User.USERNAME_FIELDS = ('phone', 'email')

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_registration'),
            {
                'phone': self.new_user_data['phone'],
                'email': self.new_user_data['email'],
                'password': self.new_user_data['password'],
                'password_2': self.new_user_data['password']
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.new_user_data['phone'],
                'password': self.new_user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)

        response = self.client.post(
            reverse('garpix_user:garpix_user_api:api_login'),
            {
                'username': self.new_user_data['email'],
                'password': self.new_user_data['password'],
            },
            HTTP_ACCEPT='application/json'
        )
        self.check_login_result(response)
