from django.db import models
from django.utils.translation import ugettext as _
from garpix_utils.string import get_random_string

from .user_session import UserSession


class ReferralType(models.Model):
    title = models.CharField(max_length=128, verbose_name=_('Referral way title'))
    referral_hash = models.CharField(max_length=32)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.referral_hash = get_random_string(32)
        super().save(force_insert, force_update, using, update_fields)


class ReferralUserLink(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE, verbose_name=_('User'))
    referral_type = models.ForeignKey(ReferralType, on_delete=models.CASCADE,
                                      verbose_name=_('Where did the user come from'))

    class Meta:
        unique_together = (('user', 'referral_type'),)
