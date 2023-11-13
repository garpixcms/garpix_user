from django.contrib.auth.password_validation import CommonPasswordValidator, MinimumLengthValidator, \
    UserAttributeSimilarityValidator
from rest_framework import serializers

from django.utils.translation import ugettext as _

from garpix_user.utils.get_password_settings import get_password_settings
from garpix_user.utils.repluralize import rupluralize


class PasswordSerializerMixin:

    def _validate_password(self, value):

        password_settings = get_password_settings()

        UserAttributeSimilarityValidator().validate(value)
        MinimumLengthValidator(min_length=password_settings['min_length']).validate(value)
        CommonPasswordValidator().validate(value)

        # check for min digits number
        password_digits_num = sum(c.isdigit() for c in value)
        if password_digits_num < password_settings['min_digits']:
            raise serializers.ValidationError(
                _('Password must contain at least {min_digits} {digits}.').format(
                    min_digits=password_settings['min_digits'],
                    digits=rupluralize(password_settings['min_digits'],
                                       _('digit,digits')))
            )

        # check for min char number
        password_chars_num = sum(c.isalpha() for c in value)
        if password_chars_num < password_settings['min_chars']:
            raise serializers.ValidationError(
                _('Password must contain at least {min_chars} {chars}.').format(
                    min_chars=password_settings['min_chars'],
                    chars=rupluralize(password_settings['min_chars'],
                                      _('char,chars')))
            )

        # check for uppercase letter
        if sum(c.isupper() for c in value) < password_settings['min_uppercase']:
            raise serializers.ValidationError(
                _('Password must contain at least {min_uppercase} uppercase {letters}.').format(
                    min_uppercase=password_settings['min_uppercase'],
                    letters=rupluralize(password_settings['min_uppercase'], _('letter,letters')))
            )

        # check for special symbols
        if (len(value) - (password_digits_num + password_chars_num)) < password_settings['min_special_symbols']:
            raise serializers.ValidationError(
                _('Password must contain at least {min_special_symbols} special {symbols}.').format(
                    min_special_symbols=password_settings['min_special_symbols'],
                    symbols=rupluralize(password_settings['min_special_symbols'], _('symbol,symbols')))
            )
