from django.db import models

from garpix_user.mixins.models import RestorePasswordMixin
from garpix_user.mixins.models.confirm import UserEmailConfirmMixin, UserPhoneConfirmMixin


class UserSessionMixin(RestorePasswordMixin, UserEmailConfirmMixin, UserPhoneConfirmMixin):

    email = models.EmailField(verbose_name='Email', null=True, blank=True)

    class Meta:
        abstract = True
