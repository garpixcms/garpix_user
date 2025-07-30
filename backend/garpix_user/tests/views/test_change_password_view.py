from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from ...models import GarpixUserPasswordConfiguration, PasswordHistory

User = get_user_model()


class ChangePasswordViewTest(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        config = GarpixUserPasswordConfiguration.get_solo()
        config.password_history = 1
        config.save()

    def setUp(self):
        self.username = 'testuser1'
        self.password = 'Old-Password123!'
        self.new_password = 'New-Password123!'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()

    def test_change_password_with_incorrect_password(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            '/api/garpix_user/change_password/',
            {
                'password': 'incorrect-password',
                'new_password': self.new_password,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
            'password': ['Password is incorrect'],
        })

    def test_change_password_with_same_password(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            '/api/garpix_user/change_password/',
            {
                'password': self.password,
                'new_password': self.password,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
            'non_field_errors': ['New password must be different from the old one'],
        })

    def test_change_password_with_old_used_password(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            '/api/garpix_user/change_password/',
            {
                'password': self.password,
                'new_password': self.new_password,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/api/garpix_user/change_password/',
            {
                'password': self.new_password,
                'new_password': self.password,
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/api/garpix_user/change_password/',
            {
                'password': self.password,
                'new_password': self.new_password,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
            'new_password': ['You can not use the same password you already had to'],
        })

    def test_change_password(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            '/api/garpix_user/change_password/',
            {
                'password': self.password,
                'new_password': self.new_password,
            },
        )

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password(self.new_password))
        self.assertEqual(1, PasswordHistory.objects.filter(user=self.user).count())

    def test_change_password_unauthorized_with_invalid_creds(self):
        response = self.client.post(
            '/api/garpix_user/change_password_unauthorized/',
            {
                'username': 'unexisting',
                'password': self.password,
                'new_password': self.new_password,
                'new_password_2': self.new_password
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
            'non_field_errors': ['Unable to log in with provided credentials.'],
        })

    def test_change_password_unauthorized_with_blocked_account(self):
        self.user.is_blocked = True
        self.user.save()

        response = self.client.post(
            '/api/garpix_user/change_password_unauthorized/',
            {
                'username': self.username,
                'password': self.password,
                'new_password': self.new_password,
                'new_password_2': self.new_password
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {
            'non_field_errors': ['Your account is blocked. Please contact your administrator'],
        })

    def test_change_password_unauthorized(self):
        self.user.needs_password_update = True
        self.user.save()

        response = self.client.post(
            '/api/garpix_user/change_password_unauthorized/',
            {
                'username': self.username,
                'password': self.password,
                'new_password': self.new_password,
                'new_password_2': self.new_password
            },
        )
        data = response.json()

        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password(self.new_password))
        self.assertEqual(1, PasswordHistory.objects.filter(user=self.user).count())
        self.assertFalse(self.user.needs_password_update)
        self.assertTrue('access_token' in data)
        self.assertTrue('refresh_token' in data)
