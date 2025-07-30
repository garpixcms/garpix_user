from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from garpix_user.models import ReferralType

BASE_GARPIX_USER_SETTINGS = getattr(settings, 'GARPIX_USER', dict())


class ReferralLinkViewTest(TestCase):
    def test_referral_links_valid(self):
        referral_link = ReferralType.objects.create(title='test_link')
        response = self.client.get(
            reverse('garpix_user:referral_link', kwargs={'hash': referral_link.referral_hash})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{BASE_GARPIX_USER_SETTINGS.get('REFERRAL_REDIRECT_URL', '/')}?status=success")

    def test_referral_links_invalid(self):
        response = self.client.get(
            reverse('garpix_user:referral_link', kwargs={'hash': 'hash'})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{BASE_GARPIX_USER_SETTINGS.get('REFERRAL_REDIRECT_URL', '/')}?status=error")
