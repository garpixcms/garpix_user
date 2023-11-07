from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


class PasswordHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    password = models.CharField(_('password'), max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))

    class Meta:
        verbose_name = _('Password history')
        verbose_name_plural = _('Password history')
