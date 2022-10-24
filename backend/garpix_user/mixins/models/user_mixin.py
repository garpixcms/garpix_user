from django.contrib.auth.models import AbstractUser
from django.db import models
from garpix_notify.mixins import UserNotifyMixin
from phonenumber_field.modelfields import PhoneNumberField

from garpix_user.mixins.models.confirm import UserEmailConfirmMixin, UserPhoneConfirmMixin
from django.db.utils import IntegrityError
from django.utils.translation import gettext as _


class GarpixUserMixin(UserEmailConfirmMixin, UserPhoneConfirmMixin, UserNotifyMixin, AbstractUser):
    new_email = models.EmailField(_("New email"), blank=True, null=True)
    new_phone = PhoneNumberField(_("New phone number"), unique=True, blank=True, null=True)

    USERNAME_FIELDS = ('username',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.USERNAME_FIELDS) == 0:
            raise IntegrityError(_('USERNAME_FIELDS can\'t be empty'))
        for field in self.USERNAME_FIELDS:
            if field not in ('email', 'phone', 'username'):
                raise IntegrityError(_(f'{field} can\'t be used as USERNAME_FIELDS. Only ("email", "phone", "username") supported'))
