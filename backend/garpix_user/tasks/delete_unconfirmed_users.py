from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.module_loading import import_string


celery_app = import_string(settings.GARPIXCMS_CELERY_SETTINGS)
GARPIX_USER_SETTINGS = getattr(settings, "GARPIX_USER", {})


@celery_app.task()
def delete_unconfirmed_users():
    User = get_user_model()
    filters_data = Q()
    delay_date = datetime.now() - timedelta(days=GARPIX_USER_SETTINGS.get('CONFIRMATION_DELAY', 10))
    if 'email' in User.USERNAME_FIELDS:
        filters_data |= Q(is_email_confirmed=False, date_joined__lt=delay_date)
    if 'phone' in User.USERNAME_FIELDS:
        filters_data |= Q(is_phone_confirmed=False, date_joined__lt=delay_date)

    if filters_data:
        User.objects.filter(filters_data).delete()


celery_app.conf.beat_schedule.update({
    'user_periodic_task': {
        'task': 'garpix_user.tasks.delete_unconfirmed_users.delete_unconfirmed_users',
        'schedule': 3600,
    }
})
celery_app.conf.timezone = 'UTC'
