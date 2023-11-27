from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.translation import gettext as _
from garpix_utils.string import get_random_string
import string
from datetime import datetime, timezone, timedelta

from garpix_user.exceptions import NotConfirmedException
from garpix_user.exceptions import IncorrectCodeException, NoTimeLeftException, WaitException, UserUnregisteredException


class RestorePasswordMixin(models.Model):
    class RESTORE_BY(models.TextChoices):
        PHONE = ('phone', _('Phone number'))
        EMAIL = ('email', _('Email'))

    restore_password_confirm_code = models.CharField(_('Restore password code'),
                                                     max_length=15, null=True, blank=True)
    is_restore_code_confirmed = models.BooleanField(_('Restore code confirmed'), blank=True, default=False)
    restore_date = models.DateTimeField(_('Restore code sent date'), null=True)
    restore_by = models.CharField(choices=RESTORE_BY.choices, default=RESTORE_BY.EMAIL, max_length=5)

    def _check_and_get_user(self, username):

        User = get_user_model()

        USERNAME_FIELDS = getattr(User, 'USERNAME_FIELDS', ('email',))

        user_data = {'keycloak_auth_only': False}

        for field in USERNAME_FIELDS:
            user_data.update({field: username})
            if field != 'username':
                user_data.update({f'is_{field}_confirmed': True})

        if user := User.active_objects.filter(**user_data).first():
            return True, user

        return False, UserUnregisteredException(field='username',
                                                extra_data={'value': username})

    def _check_request_time(self):

        if (TIME_LAST_REQUEST := settings.GARPIX_USER.get('TIME_LAST_REQUEST', 1)) and (
                restore_date := self.restore_date):
            if restore_date + timedelta(minutes=TIME_LAST_REQUEST) >= datetime.now(restore_date.tzinfo):
                return False, WaitException()

        return True, None

    def _time_is_up(self):
        datediff = datetime.now(self.restore_date.tzinfo) - self.restore_date

        if self.restore_by == self.RESTORE_BY.EMAIL:
            datediff = datediff.days if settings.GARPIX_USER.get('CONFIRM_EMAIL_CODE_LIFE_TIME_TYPE',
                                                                 'days') == 'days' else datediff.seconds / 60
            return datediff > settings.GARPIX_USER.get(
                'CONFIRM_EMAIL_CODE_LIFE_TIME', 6)
        return datediff.seconds / 60 > settings.GARPIX_USER.get(
            'CONFIRM_PHONE_CODE_LIFE_TIME', 6)

    def send_restore_code(self, username=None):
        from garpix_notify.models import Notify

        result, data = self._check_and_get_user(username)
        if not result:
            return result, data
        user = data
        result, error = self._check_request_time()
        if not result:
            return result, error

        confirmation_code = get_random_string(settings.GARPIX_USER.get('CONFIRM_CODE_LENGTH', 6), string.digits)

        self.restore_password_confirm_code = confirmation_code
        self.restore_date = datetime.now(timezone.utc)
        self.is_restore_code_confirmed = False

        if user.email == username and 'email' in user.USERNAME_FIELDS:
            Notify.send(settings.RESTORE_PASSWORD_EMAIL_EVENT, {
                'user': user,
                'restore_code': self.restore_password_confirm_code
            }, email=user.email)
            self.restore_by = self.RESTORE_BY.EMAIL
            self.email = username
        elif 'phone' in user.USERNAME_FIELDS:
            Notify.send(settings.RESTORE_PASSWORD_PHONE_EVENT, {
                'user': user,
                'restore_code': self.restore_password_confirm_code
            }, phone=user.phone)
            self.restore_by = self.RESTORE_BY.PHONE
            self.phone = username

        self.save()

        return True, None

    def check_restore_code(self, username, restore_password_confirm_code=None):

        if getattr(self,
                   self.restore_by) != username or self.restore_password_confirm_code != restore_password_confirm_code:
            return False, IncorrectCodeException(field='restore_password_confirm_code')

        time_is_up = self._time_is_up()

        if time_is_up:
            return False, NoTimeLeftException(field='restore_password_confirm_code')

        self.is_restore_code_confirmed = True
        self.save()

        return True, None

    def restore_password(self, new_password, username, restore_password_confirm_code=None):
        User = get_user_model()

        USERNAME_FIELDS = getattr(User, 'USERNAME_FIELDS', ('email',))

        field_name = '/'.join([User._meta.get_field(
            field).verbose_name.title().lower() for field in USERNAME_FIELDS]).rstrip('/')

        if self.is_restore_code_confirmed and restore_password_confirm_code == self.restore_password_confirm_code and getattr(
                self, self.restore_by) == username:

            time_is_up = self._time_is_up()

            if time_is_up:
                return False, NoTimeLeftException(field='restore_password_confirm_code')

            result, data = self._check_and_get_user(username)
            if not result:
                return result, data

            with transaction.atomic():
                user = data
                user.set_password(new_password)
                user.save()
                self.is_restore_code_confirmed = False
                self.save()
            return True, None
        return False, NotConfirmedException(
            extra_data={'field': field_name})

    class Meta:
        abstract = True
