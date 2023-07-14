import string

from django.conf import settings
from django.db import models
from datetime import datetime, timedelta

from django.urls import reverse
from django.utils.translation import ugettext as _
import hashlib
from garpix_utils.string import get_random_string

from garpix_user.mixins.models.confirm.code_length_mixin import CodeLengthMixin
from garpix_user.utils.current_date import set_current_date


class UserEmailConfirmMixin(CodeLengthMixin, models.Model):
    """
    Миксин для подтверждения email
    """

    email_confirmation_code = models.CharField(_("Email confirmation code"), max_length=255, blank=True,
                                               null=True)
    email_code_send_date = models.DateTimeField(_("Code sent date"), blank=True, null=True)
    email_confirmed_date = models.DateTimeField(_("Date email was confirmed"), blank=True, null=True)
    new_email = models.EmailField(_("New email"), blank=True, null=True)

    def send_email_confirmation_link(self):
        from garpix_notify.models import Notify
        from garpix_user.models import UserSession
        from django.contrib.auth import get_user_model

        User = get_user_model()

        model_type = 'user_session' if isinstance(self, UserSession) else 'user'
        hash = str(
            hashlib.sha512(f'{self.email}+{self.email_confirmation_code}'.encode("utf-8")).hexdigest()).lower()
        Notify.send(settings.EMAIL_LINK_CONFIRMATION_EVENT, {
            'confirmation_link': User.confirm_link_redirect_url(model_type, hash)
        }, email=self.new_email)

    def send_email_confirmation_code(self, email=None):
        from django.contrib.auth import get_user_model
        from garpix_user.exceptions import UserRegisteredException, WaitException
        from garpix_notify.models import Notify

        User = get_user_model()

        anybody_have_this_email = User.objects.filter(email=email)
        if isinstance(self, User):
            anybody_have_this_email = anybody_have_this_email.exclude(id=self.id)
        if anybody_have_this_email.count() > 0:
            return UserRegisteredException(field='email', extra_data={
                'field': self._meta.get_field('email').verbose_name.title().lower()})

        if settings.GARPIX_USER.get('TIME_LAST_REQUEST', None):
            if self.email_code_send_date and self.email_code_send_date + timedelta(
                    minutes=settings.GARPIX_USER.get('TIME_LAST_REQUEST')) >= datetime.now(
                self.email_code_send_date.tzinfo):
                return WaitException()

        confirmation_code = get_random_string(self.get_confirm_code_length('email'), string.digits)

        self.new_email = email or self.email

        self.email_confirmation_code = confirmation_code

        self.email_code_send_date = set_current_date()

        self.save()

        if settings.GARPIX_USER.get('USE_EMAIL_LINK_CONFIRMATION', True):
            self.send_email_confirmation_link()
        else:
            Notify.send(settings.EMAIL_CONFIRMATION_EVENT, {
                'confirmation_code': confirmation_code
            }, email=self.new_email)

        return True

    def confirm_email(self, email_confirmation_code):
        from garpix_user.exceptions import IncorrectCodeException, NoTimeLeftException

        if self.email_confirmation_code != email_confirmation_code:
            return IncorrectCodeException(field='email_confirmation_code')

        datediff = datetime.now(self.email_code_send_date.tzinfo) - self.email_code_send_date
        datediff = datediff.days if settings.GARPIX_USER.get('CONFIRM_EMAIL_CODE_LIFE_TIME_TYPE',
                                                             'days') == 'days' else datediff.seconds / 60

        time_is_up = datediff > settings.GARPIX_USER.get(
            'CONFIRM_EMAIL_CODE_LIFE_TIME', 6)

        if time_is_up:
            return NoTimeLeftException(field='email_confirmation_code')

        self.is_email_confirmed = True
        self.email = self.new_email
        self.email_confirmation_code = None
        self.email_confirmed_date = set_current_date()
        self.save()
        return True

    @classmethod
    def confirm_email_by_link(cls, hash):
        from garpix_user.exceptions import IncorrectCodeException, NoTimeLeftException

        users_list = cls.objects.all()

        for user in users_list:
            if str(hashlib.sha512(
                    f'{user.email}+{user.email_confirmation_code}'.encode("utf-8")).hexdigest()).lower() == hash:
                datediff = datetime.now(user.email_code_send_date.tzinfo) - user.email_code_send_date
                datediff = datediff.days if settings.GARPIX_USER.get('CONFIRM_EMAIL_CODE_LIFE_TIME_TYPE',
                                                                     'days') == 'days' else datediff.seconds / 60
                time_is_up = datediff > settings.GARPIX_USER.get('CONFIRM_EMAIL_CODE_LIFE_TIME', 6)
                if time_is_up:
                    return False, NoTimeLeftException(field='email_confirmation_code')
                user.is_email_confirmed = True
                user.email = user.new_email or user.email
                user.email_confirmation_code = None
                user.save()
                return True, user

        return False, IncorrectCodeException(field='email_confirmation_code')

    def check_email_confirmation(self):
        return self.is_email_confirmed and self.email_confirmed_date and self.email_confirmed_date + timedelta(
            days=settings.GARPIX_USER.get('EMAIL_CONFIRMATION_LIFE_TIME', 2)) >= datetime.now(
            self.email_confirmed_date.tzinfo)

    @classmethod
    def confirm_link_redirect_url(cls, model_type, hash):
        return reverse('garpix_user:email_confirmation_link', args=[model_type, hash])

    class Meta:
        abstract = True
