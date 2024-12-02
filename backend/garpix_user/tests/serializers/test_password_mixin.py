from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.test import APITestCase
from ...mixins.serializers.password_mixin import PasswordSerializerMixin
from ...models import GarpixUserPasswordConfiguration

User = get_user_model()


class PasswordSerializerMixinTest(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        config = GarpixUserPasswordConfiguration.get_solo()
        config.min_length = 8
        config.min_digits = 3
        config.min_chars = 3
        config.min_uppercase = 1
        config.min_special_symbols = 1
        config.save()

        cls.mixin = PasswordSerializerMixin()

    def test_validate_password_common_invalid(self):
        with self.assertRaises(ValidationError, msg='This password is too common.'):
            self.mixin._validate_password('12345678')

    def test_validate_password_min_length_invalid(self):
        with self.assertRaises(ValidationError, msg='This password is too short. It must contain at least 8 characters.'):
            self.mixin._validate_password('1234')

    def test_validate_password_min_digits_invalid(self):
        with self.assertRaises(serializers.ValidationError, msg='Password must contain at least 3 digits.'):
            self.mixin._validate_password('12SfxLB!')

    def test_validate_password_min_chars_invalid(self):
        with self.assertRaises(serializers.ValidationError, msg='Password must contain at least 3 chars.'):
            self.mixin._validate_password('19219LB!')

    def test_validate_password_min_uppercase_invalid(self):
        with self.assertRaises(serializers.ValidationError, msg='Password must contain at least 1 uppercase letters.'):
            self.mixin._validate_password('1921xlb!')

    def test_validate_password_min_special_symbols_invalid(self):
        with self.assertRaises(serializers.ValidationError, msg='Password must contain at least 1 special symbols.'):
            self.mixin._validate_password('1921xlb0')

    def test_validate_password_valid(self):
        self.assertIsNone(self.mixin._validate_password('1921Bxb0!'))
