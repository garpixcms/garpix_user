from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from garpix_user.models import ReferralType

BASE_GARPIX_USER_SETTINGS = getattr(settings, 'GARPIX_USER', dict())


class LoginViewTest(TestCase):
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
