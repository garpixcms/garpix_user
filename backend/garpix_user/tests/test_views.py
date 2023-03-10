from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from garpix_user.models import ReferralType

User = get_user_model()
BASE_GARPIX_USER_SETTINGS = getattr(settings, 'GARPIX_USER', dict())


class LoginViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser1'
        self.password = '12345'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()

    def test_invalid_username_password(self):
        response = self.client.post(
            reverse('authorize'),
            {
                'username': self.username,
                'password': 'passwordtest',
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.content, b'{"__all__": ["Invalid: username / password"]}')

    def test_valid_username_password(self):
        response = self.client.post(
            reverse('authorize'),
            {
                'username': self.username,
                'password': self.password,
            },
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_valid_redirects(self):
        response = self.client.post(
            reverse('authorize'),
            {
                'username': self.username,
                'password': self.password,
            },
        )
        self.assertRedirects(response, '/')

    def test_referral_links(self):
        """
        Check referral links functionality
        """
        if BASE_GARPIX_USER_SETTINGS.get('USE_REFERRAL_LINKS', False):
            referral_link = ReferralType.objects.create(title='test_link')
            response = self.client.get(
                reverse('garpix_user:referral_link', args=[referral_link.referral_hash])
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response,
                                 f"{BASE_GARPIX_USER_SETTINGS.get('REFERRAL_REDIRECT_URL', '/')}?status=success")
