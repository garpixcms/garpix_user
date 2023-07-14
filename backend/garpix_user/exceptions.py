from django.conf import settings
from django.core.validators import ValidationError
from django.utils.translation import ugettext as _
from rest_framework import serializers

from garpix_user.utils.repluralize import rupluralize


class ModelException(Exception):
    code = 'invalid'
    field = None

    def __init__(self, field=None, extra_data={}):
        self.message = self.get_message().format(**extra_data)
        self.field = field

    def raise_exception(self, exception_class=ValidationError):
        field = self.field or 'non_field_errors'
        raise exception_class({field: [self.message]}, code=self.code)

    def get_message(self):
        return ''


class WaitException(ModelException):
    def get_message(self):
        return settings.GARPIX_USER.get('WAIT_RESPONSE',
                                        _("Less than {min_time} {minutes} has passed since the last request")).format(
            min_time=settings.GARPIX_USER.get('TIME_LAST_REQUEST', 1),
            minutes=rupluralize(settings.GARPIX_USER.get('TIME_LAST_REQUEST', 1), _('minute,minutes')))


class UserRegisteredException(ModelException):
    def get_message(self):
        return settings.GARPIX_USER.get('USER_REGISTERED_RESPONSE',
                                        _("User with such data has been already registered"))


class UserUnregisteredException(ModelException):
    def get_message(self):
        return settings.GARPIX_USER.get('USER_UNREGISTERED_RESPONSE', _("User with such data has not been registered"))


class IncorrectCodeException(ModelException):
    def get_message(self):
        return _("Incorrect code")


class NoTimeLeftException(ModelException):
    def get_message(self):
        return _("Code has expired. Request it again")


class NotAuthenticateException(ModelException):
    def get_message(self):
        return _("Credentials were not provided")


class NotConfirmedException(ModelException):
    def get_message(self):
        return _("{field} was not confirmed")


class ValidationErrorSerializer(serializers.Serializer):
    field = serializers.ListField(default=['Error'])
