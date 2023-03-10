from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from garpix_notify.mixins import UserNotifyMixin
from garpix_utils.managers import ActiveManager
from garpix_utils.models import DeleteMixin
from garpix_utils.string import get_random_string
from phonenumber_field.modelfields import PhoneNumberField

from garpix_user.mixins.models.confirm import UserEmailConfirmMixin, UserPhoneConfirmMixin
from django.db.utils import IntegrityError
from django.utils.translation import gettext as _
import string

from garpix_user.utils.current_date import set_current_date


class GarpixUser(DeleteMixin, UserEmailConfirmMixin, UserPhoneConfirmMixin, UserNotifyMixin, AbstractUser):
    is_email_confirmed = models.BooleanField(_("Email confirmed"), default=True)

    phone = PhoneNumberField(_("Phone number"), blank=True, default='')
    is_phone_confirmed = models.BooleanField(_("Phone number confirmed"), default=True)

    USERNAME_FIELDS = ('username',)

    objects = UserManager()
    active_objects = ActiveManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = True

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        GARPIX_USER_SETTINGS = getattr(settings, "GARPIX_USER", {})

        if is_new and not self.is_email_confirmed and GARPIX_USER_SETTINGS.get('USE_EMAIL_CONFIRMATION', False) and GARPIX_USER_SETTINGS.get(
                'USE_EMAIL_LINK_CONFIRMATION', True):

            confirmation_code = get_random_string(self.get_confirm_code_length('email'), string.digits)

            self.email_confirmation_code = confirmation_code
            self.email_code_send_date = set_current_date()
            self.new_email = self.email
            self.send_email_confirmation_link()

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.is_active = False
        self.save()

    def __str__(self):
        return f'{self.first_name}, {self.last_name}' if self.first_name or self.last_name else self.email or str(self.phone)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.USERNAME_FIELDS) == 0:
            raise IntegrityError(_('USERNAME_FIELDS can\'t be empty'))
        for field in self.USERNAME_FIELDS:
            if field not in ('email', 'phone', 'username'):
                raise IntegrityError(
                    _(f'{field} can\'t be used as USERNAME_FIELDS. Only ("email", "phone", "username") supported'))

    def set_user_session(self, request):
        from garpix_user.models import UserSession
        current_user_session = UserSession.get_from_request(request)
        if current_user_session:
            if (user_user_session := UserSession.objects.filter(
                    user=self).first()) and user_user_session != current_user_session:
                current_user_session.delete()
            else:
                current_user_session.user = self
                current_user_session.recognized = UserSession.UserState.REGISTERED
                current_user_session.save()
