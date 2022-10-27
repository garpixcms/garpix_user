from django.test import TestCase

from django.contrib.auth import get_user_model


class ApiTestMixin(TestCase):
    def set_init_data(self):
        self.User = get_user_model()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'phone': '+79999999999',
            'password': 'q1W2e3R4t5Y6'
        }
        self.new_user_data = {
            'username': 'testuser1',
            'email': 'test1@gmail.com',
            'phone': '+79999999998',
            'password': 'q1W2e3R4t5Y6'
        }
        self.user = self.User.objects.create_user(**self.user_data)

        self.user.save()

    def user_login(self):
        self.client.force_login(self.user)
        self.client.force_authenticate(self.user)

    def check_login_result(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        self.assertNotEqual(response.json()['access_token'], '')
        self.assertIn('access_token_expires', response.json())
        self.assertIn('refresh_token', response.json())
        self.assertNotEqual(response.json()['refresh_token'], '')
        self.assertIn('refresh_token_expires', response.json())
        self.assertIn('token_type', response.json())
