from django.conf import settings
from django.views.generic import RedirectView

from garpix_user.models import UserSession, ReferralType, ReferralUserLink


class ReferralLinkView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        hash = self.kwargs.get('hash', None)
        user = UserSession.get_or_create_user_session(self.request)
        try:
            referral_instance = ReferralType.objects.get(referral_hash=hash)
            ReferralUserLink.objects.create(user=user, referral_type=referral_instance)
        except Exception:
            pass

        return settings.GARPIX_USER.get('REFERRAL_REDIRECT_URL', '/')
