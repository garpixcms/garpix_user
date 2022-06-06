from django.contrib.auth.models import AbstractUser
from garpix_notify.mixins import UserNotifyMixin
from garpix_user.mixins.models.confirm import UserEmailConfirmMixin, UserPhoneConfirmMixin


class User(UserEmailConfirmMixin, UserPhoneConfirmMixin, UserNotifyMixin, AbstractUser):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
