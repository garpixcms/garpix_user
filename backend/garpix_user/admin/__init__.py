from django.conf import settings

from .user_session import UserSessionAdmin  # noqa

from .user import UserAdmin  # noqa

from .password_history import PasswordHistoryAdmin  # noqa

from .group import GarpixGroupAdmin


if settings.GARPIX_USER.get('USE_REFERRAL_LINKS', False):
    from .referral_type import ReferralTypeAdmin  # noqa

if settings.GARPIX_USER.get('ADMIN_PASSWORD_SETTINGS', False):
    from .site_config import GarpixUserPasswordConfigurationAdmin  # noqa
