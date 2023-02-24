from django.conf import settings
from rest_framework import serializers

from django.utils.translation import ugettext as _

from garpix_user.utils.repluralize import rupluralize


class PasswordSerializerMixin:

    def _validate_password(self, value):
        GARPIX_USER_SETTINGS = settings.GARPIX_USER

        min_length = GARPIX_USER_SETTINGS.get('MIN_LENGTH_PASSWORD', 8)
        min_digits = GARPIX_USER_SETTINGS.get('MIN_DIGITS_PASSWORD', 2)
        min_chars = GARPIX_USER_SETTINGS.get('MIN_CHARS_PASSWORD', 2)
        min_uppercase = GARPIX_USER_SETTINGS.get('MIN_UPPERCASE_PASSWORD', 1)

        # check for min length
        if len(value) < min_length:
            raise serializers.ValidationError(
                _('Password must be at least {min_length} {characters} long.').format(min_length=min_length,
                                                                                      characters=rupluralize(
                                                                                          min_length,
                                                                                          _('character,characters')))
            )

        # check for min digits number
        if sum(c.isdigit() for c in value) < min_digits:
            raise serializers.ValidationError(
                _('Password must contain at least {min_digits} {digits}.').format(min_digits=min_digits,
                                                                                  digits=rupluralize(min_digits,
                                                                                                     _('digit,digits')))
            )

        # check for min char number
        if sum(c.isalpha() for c in value) < min_chars:
            raise serializers.ValidationError(
                _('Password must contain at least {min_chars} {chars}.').format(min_chars=min_chars,
                                                                                chars=rupluralize(min_chars,
                                                                                                  _('char,chars')))
            )

        # check for uppercase letter
        if sum(c.isupper() for c in value) < min_uppercase:
            raise serializers.ValidationError(
                _('Password must contain at least {min_uppercase} uppercase {letters}.').format(
                    min_uppercase=min_uppercase, letters=rupluralize(min_uppercase, _('letter,letters')))
            )
