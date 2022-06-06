from django.conf import settings

from .users_config_admin import GarpixUserConfigAdmin  # noqa

if settings.GARPIX_USER.get('USE_REFERRAL_LINKS', False):
    from .referral_type import ReferralTypeAdmin  # noqa
