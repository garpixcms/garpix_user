from django.db.models.signals import post_save
from django.dispatch import receiver

from garpix_notify.models import Notify
from user.models import User
from .settings import EMAIL_CONFIRMATION_EVENT


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        notify = Notify.send(EMAIL_CONFIRMATION_EVENT, {
            'confirmation_code': '1233213123'
        }, email=instance.email)
        return notify
