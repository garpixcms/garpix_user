from unittest.mock import MagicMock
from dataclasses import dataclass

from django.conf import settings
from rest_framework.test import APITestCase

from garpix_user.utils.get_password_settings import (
    get_password_settings,
    GarpixUserPasswordConfiguration,
)


class GetPasswordSettingsTest(APITestCase):
    @dataclass
    class settings:
        min_length = 0
        min_digits = 0
        min_chars = 0
        min_uppercase = 0
        min_special_symbols = 0
        available_attempt = 0
        password_history = 0
        password_validity_period = 0
        password_first_change = 0
        password_validity_inform_days = 0
        access_token_ttl_seconds = 0
        refresh_token_ttl_seconds = 0
        access_tokens_count = 0
    
    def test_get_password_settings(self) -> None:
        settings.GARPIX_USER["ADMIN_PASSWORD_SETTINGS"] = False
        GARPIX_USER_SETTINGS = settings.GARPIX_USER

        _access_token_ttl_seconds = getattr(settings, 'GARPIX_ACCESS_TOKEN_TTL_SECONDS', 0)
        _refresh_token_ttl_seconds = getattr(settings, 'GARPIX_REFRESH_TOKEN_TTL_SECONDS', 0)

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
        access_tokens_count = GARPIX_USER_SETTINGS.get('ACCESS_TOKENS_COUNT', -1)

        self.assertEqual(
            get_password_settings(),
            {
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
                'refresh_token_ttl_seconds': refresh_token_ttl_seconds,
                'access_tokens_count': access_tokens_count,
            }
        )

    def test_get_password_settings_admin(self) -> None:
        settings.GARPIX_USER["ADMIN_PASSWORD_SETTINGS"] = True
        GarpixUserPasswordConfiguration.get_solo = MagicMock(return_value=self.settings)
        self.assertEqual(
            get_password_settings(),
            {
                'min_length': self.settings.min_length,
                'min_digits': self.settings.min_digits,
                'min_chars': self.settings.min_chars,
                'min_uppercase': self.settings.min_uppercase,
                'min_special_symbols': self.settings.min_special_symbols,
                'available_attempt': self.settings.available_attempt,
                'password_history': self.settings.password_history,
                'password_validity_period': self.settings.password_validity_period,
                'password_first_change': self.settings.password_first_change,
                'password_validity_inform_days': self.settings.password_validity_inform_days,
                'access_token_ttl_seconds': self.settings.access_token_ttl_seconds,
                'refresh_token_ttl_seconds': self.settings.refresh_token_ttl_seconds,
                'access_tokens_count': self.settings.access_tokens_count,
            }
        )
        self.assertTrue(GarpixUserPasswordConfiguration.get_solo.called)
