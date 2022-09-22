from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from garpix_utils.string import get_random_string

import string
from datetime import datetime, timezone, timedelta


class RestorePasswordMixin(models.Model):
    restore_password_confirm_code = models.CharField(_('Restore password code'),
                                                     max_length=15, null=True, blank=True)
    is_restore_code_confirmed = models.BooleanField(_('Restore code confirmed'), default=False)
    restore_date = models.DateTimeField(_('Restore code sent date'), null=True)

    def _check_user_data(self, email, phone):
        from garpix_user.exceptions import UserUnregisteredException

        if email and (self.user is None or email != self.user.email or not self.user.is_email_confirmed):
            UserUnregisteredException(field='email',
                                      extra_data={'field': self._meta.get_field('email').verbose_name.title().lower()})

        if phone and (self.user is None or phone != self.user.phone or not self.user.is_phone_confirmed):
            UserUnregisteredException(field='phone',
                                      extra_data={'field': self._meta.get_field('phone').verbose_name.title().lower()})

    def _check_request_time(self):
        from garpix_user.exceptions import WaitException

        if (TIME_LAST_REQUEST := settings.GARPIX_USER.get('TIME_LAST_REQUEST', None)) and (restore_date := self.restore_date):
            if restore_date + timedelta(minutes=TIME_LAST_REQUEST) >= datetime.now(restore_date.tzinfo):
                return WaitException()

    def send_restore_code(self, email=None, phone=None):
        from garpix_notify.models import Notify

        self._check_user_data(email, phone)
        self._check_request_time()

        confirmation_code = get_random_string(settings.GARPIX_USER.get('CONFIRM_CODE_LENGTH', 6), string.digits)

        self.restore_password_confirm_code = confirmation_code
        self.restore_date = datetime.now(timezone.utc)
        self.save()

        if email:
            Notify.send(settings.EMAIL_RESTORE_PASSWORD_EVENT, {
                'user_fullname': str(self.user),
                'email': self.user.email,
                'restore_code': self.restore_password_confirm_code
            }, email=self.user.email)
        elif phone:
            Notify.send(settings.PHONE_RESTORE_PASSWORD_EVENT, {
                'user_fullname': str(self.user),
                'phone': self.user.phone,
                'restore_code': self.user.restore_password_confirm_code
            }, phone=self.user.phone)

        return True

    def check_restore_code(self, restore_password_confirm_code=None):
        from garpix_user.exceptions import IncorrectCodeException, NoTimeLeftException

        if self.restore_password_confirm_code != restore_password_confirm_code:
            return IncorrectCodeException(field='restore_password_confirm_code')

        time_is_up = (datetime.now(
            self.restore_date.tzinfo) - self.restore_date).seconds / 60 > settings.GARPIX_USER.get('CONFIRM_EMAIL_CODE_LIFE_TIME', 6)

        if time_is_up:
            return NoTimeLeftException(field='restore_password_confirm_code')

        self.is_restore_code_confirmed = True
        self.save()

        return True

    def restore_password(self, new_password=None):
        if self.is_restore_code_confirmed:
            self.user.set_password(new_password)
            self.user.save()
            return True
        return False

    class Meta:
        abstract = True
