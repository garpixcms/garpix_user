from django.conf import settings

from .user_session import UserSessionAdmin  # noqa

from .user import UserAdmin  # noqa

if settings.GARPIX_USER.get('USE_REFERRAL_LINKS', False):
    from .referral_type import ReferralTypeAdmin  # noqa
