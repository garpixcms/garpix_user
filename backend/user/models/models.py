from django.contrib.auth.models import AbstractUser
from garpix_notify.mixins import UserNotifyMixin
from garpix_auth.models.confirm import UserPhoneConfirmMixin
from garpix_auth.models import RestorePasswordMixin


class User(AbstractUser, UserNotifyMixin, UserPhoneConfirmMixin, RestorePasswordMixin):
    pass

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
