from datetime import datetime, timedelta

from celery.schedules import crontab
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string
from garpix_notify.models import SystemNotify
from django.utils.translation import gettext_lazy as _
from garpix_user.utils.get_password_settings import get_password_settings

celery_app = import_string(settings.GARPIXCMS_CELERY_SETTINGS)


@celery_app.task()
def password_validity_passed():
    password_settings = get_password_settings()
    _password_validity_period = password_settings['password_validity_period']
    _password_validity_inform_days = password_settings['password_validity_inform_days']
    if _password_validity_period != -1 and _password_validity_inform_days != -1:
        password_validity_period = datetime.now() - timedelta(
            days=(_password_validity_inform_days + _password_validity_period))
        inform_users = get_user_model().active_objects.filter(password_updated_date__lte=password_validity_period)

        for user in inform_users:
            SystemNotify.send({
                'message': {
                    'message': _(
                        'Your password will expire in {days} days. Please change your password').format(
                        days=(user.password_updated_date + timedelta(days=_password_validity_period)).days)
                },
                'event': settings.NOTIFY_PASSWORD_INVALID_EVENT
            }, user, event=settings.NOTIFY_PASSWORD_INVALID_EVENT, room_name=f'workflow-{user.pk}')


celery_app.conf.beat_schedule.update({
    'password_validity_passed': {
        'task': 'garpix_user.tasks.password_validity_passed.password_validity_passed',
        'schedule': crontab(minute='0', hour='21'),
    }
})
celery_app.conf.timezone = 'UTC'
