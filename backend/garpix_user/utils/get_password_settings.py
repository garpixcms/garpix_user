from django.conf import settings

from garpix_user.models import GarpixUserPasswordConfiguration


def get_password_settings():
    GARPIX_USER_SETTINGS = settings.GARPIX_USER

    _access_token_ttl_seconds = getattr(settings, 'GARPIX_ACCESS_TOKEN_TTL_SECONDS', 0)  # DEPRECATED
    _refresh_token_ttl_seconds = getattr(settings, 'GARPIX_REFRESH_TOKEN_TTL_SECONDS', 0)  # DEPRECATED

    if GARPIX_USER_SETTINGS.get('ADMIN_PASSWORD_SETTINGS', False):
        admin_password_settings = GarpixUserPasswordConfiguration.get_solo()
        min_length = admin_password_settings.min_length
        min_digits = admin_password_settings.min_digits
        min_chars = admin_password_settings.min_chars
        min_uppercase = admin_password_settings.min_uppercase
        min_special_symbols = admin_password_settings.min_special_symbols
        available_attempt = admin_password_settings.available_attempt
        password_history = admin_password_settings.password_history
        password_validity_period = admin_password_settings.password_validity_period
        password_first_change = admin_password_settings.password_first_change
        password_validity_inform_days = admin_password_settings.password_validity_inform_days
        access_token_ttl_seconds = admin_password_settings.access_token_ttl_seconds
        refresh_token_ttl_seconds = admin_password_settings.refresh_token_ttl_seconds
    else:
        min_length = GARPIX_USER_SETTINGS.get('MIN_LENGTH_PASSWORD', 8)
        min_digits = GARPIX_USER_SETTINGS.get('MIN_DIGITS_PASSWORD', 2)
        min_chars = GARPIX_USER_SETTINGS.get('MIN_CHARS_PASSWORD', 2)
        min_uppercase = GARPIX_USER_SETTINGS.get('MIN_UPPERCASE_PASSWORD', 1)
        min_special_symbols = GARPIX_USER_SETTINGS.get('MIN_SPECIAL_PASSWORD', 1)
        available_attempt = GARPIX_USER_SETTINGS.get('AVAILABLE_ATTEMPT', -1)
        password_history = GARPIX_USER_SETTINGS.get('PASSWORD_HISTORY', -1)
        password_validity_period = GARPIX_USER_SETTINGS.get('PASSWORD_VALIDITY_PERIOD', -1)
        password_first_change = GARPIX_USER_SETTINGS.get('PASSWORD_FIRST_CHANGE', False)
        password_validity_inform_days = GARPIX_USER_SETTINGS.get('PASSWORD_VALIDITY_INFORM_DAYS', -1)
        access_token_ttl_seconds = GARPIX_USER_SETTINGS.get('ACCESS_TOKEN_TTL_SECONDS', _access_token_ttl_seconds)
        refresh_token_ttl_seconds = GARPIX_USER_SETTINGS.get('REFRESH_TOKEN_TTL_SECONDS', _refresh_token_ttl_seconds)

    return {
        'min_length': min_length,
        'min_digits': min_digits,
        'min_chars': min_chars,
        'min_uppercase': min_uppercase,
        'min_special_symbols': min_special_symbols,
        'available_attempt': available_attempt,
        'password_history': password_history,
        'password_validity_period': password_validity_period,
        'password_first_change': password_first_change,
        'password_validity_inform_days': password_validity_inform_days,
        'access_token_ttl_seconds': access_token_ttl_seconds,
        'refresh_token_ttl_seconds': refresh_token_ttl_seconds
    }
