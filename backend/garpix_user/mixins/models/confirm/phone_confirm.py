import string
from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from garpix_utils.string import get_random_string
from phonenumber_field.modelfields import PhoneNumberField

from garpix_user.mixins.models.confirm.code_length_mixin import CodeLengthMixin


class UserPhoneConfirmMixin(CodeLengthMixin, models.Model):
    """
    Миксин для подтверждения номера телефона
    """

    phone_confirmation_code = models.CharField(_('Phone confirmation code'), max_length=15,
                                               blank=True, null=True)
    phone_code_send_date = models.DateTimeField(_("Code sent date"), blank=True, null=True)
    phone_confirmed_date = models.DateTimeField(_("Date phone was confirmed"), blank=True, null=True)
    new_phone = PhoneNumberField(_("New phone number"), unique=True, blank=True, null=True)

    def send_phone_confirmation_code(self, phone=None):
        from garpix_user.exceptions import UserRegisteredException, WaitException
        from garpix_notify.models import Notify

        User = get_user_model()

        anybody_have_this_phone = User.objects.filter(phone=phone)
        if isinstance(self, User):
            anybody_have_this_phone = anybody_have_this_phone.exclude(id=self.id)
        if anybody_have_this_phone.count() > 0:
            return UserRegisteredException(field='phone', extra_data={'field': self._meta.get_field('phone').verbose_name.title().lower()})

        if settings.GARPIX_USER.get('TIME_LAST_REQUEST', None):
            if self.phone_code_send_date and self.phone_code_send_date + timedelta(
                    minutes=settings.GARPIX_USER.get('TIME_LAST_REQUEST')) >= datetime.now(self.phone_code_send_date.tzinfo):
                return WaitException()

        confirmation_code = get_random_string(self.get_confirm_code_length('phone'), string.digits)

        self.new_phone = phone or self.phone

        self.phone_confirmation_code = confirmation_code

        try:
            self.phone_code_send_date = timezone.now()
        except Exception:
            self.phone_code_send_date = datetime.now()

        self.save()

        Notify.send(settings.PHONE_CONFIRMATION_EVENT, {
            'confirmation_code': confirmation_code
        }, phone=self.new_phone)

        return True

    def confirm_phone(self, phone_confirmation_code):
        from garpix_user.exceptions import IncorrectCodeException, NoTimeLeftException

        if self.phone_confirmation_code != phone_confirmation_code:
            return IncorrectCodeException(field='phone_confirmation_code')

        time_is_up = (datetime.now(
            self.phone_code_send_date.tzinfo) - self.phone_code_send_date).seconds / 60 > settings.GARPIX_USER.get('CONFIRM_PHONE_CODE_LIFE_TIME', 6)

        if time_is_up:
            return NoTimeLeftException(field='phone_confirmation_code')

        self.is_phone_confirmed = True
        self.phone_confirmation_code = None
        self.phone = self.new_phone
        self.save()
        return True

    def check_phone_confirmation(self):
        return self.is_phone_confirmed and self.phone_confirmed_date and self.phone_confirmed_date + timedelta(
                days=settings.GARPIX_USER.get('PHONE_CONFIRMATION_LIFE_TIME', 2)) >= datetime.now(
            self.phone_confirmed_date.tzinfo)

    class Meta:
        abstract = True
