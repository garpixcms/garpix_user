from django.conf import settings
from django.core.validators import ValidationError
from django.utils.translation import ugettext as _
from rest_framework import serializers


class ModelException(Exception):
    message = ''
    code = 'invalid'
    field = None

    def __init__(self, field=None, extra_data={}):
        self.message = self.message.format(**extra_data)
        self.field = field

    def raise_exception(self, exception_class=ValidationError):
        field = self.field or 'non_field_error'
        raise exception_class({field: [self.message]}, code=self.code)

    def get_message(self):
        return self.message


class WaitException(ModelException):
    message = settings.GARPIX_USER.get('WAIT_RESPONSE',
                                       _("Less than {min_time} minutes has passed since the last request")).format(
        min_time=settings.GARPIX_USER.get('GARPIX_TIME_LAST_REQUEST', 1))


class UserRegisteredException(ModelException):
    message = settings.GARPIX_USER.get('USER_REGISTERED_RESPONSE',
                                       _("User with such {field} has been already registered"))


class UserUnregisteredException(ModelException):
    message = settings.GARPIX_USER.get('USER_UNREGISTERED_RESPONSE', _("User on {value} has not been registered"))


class IncorrectCodeException(ModelException):
    message = _("Incorrect code")


class NoTimeLeftException(ModelException):
    message = _("Code has expired. Request it again")


class NotAuthenticateException(ModelException):
    message = _("Credentials were not provided")


class NotConfirmedException(ModelException):
    message = _("{field} was not confirmed")


class ValidationErrorSerializer(serializers.Serializer):
    field = serializers.ListField(default=['Error'])
