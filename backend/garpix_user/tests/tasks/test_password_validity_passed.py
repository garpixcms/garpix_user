from typing import Any
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from rest_framework.test import APITestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from model_bakery import baker

from garpix_notify.models import SystemNotify
from garpix_user.utils.repluralize import rupluralize
from garpix_user.tasks.password_validity_passed import password_validity_passed


User = get_user_model()


class PasswordValidityPassed(APITestCase):
    def setUp(self) -> None:
        self._delete_all_users()
        settings.GARPIX_USER["ADMIN_PASSWORD_SETTINGS"] = False

    def test_password_validity_passed_expired(self) -> None:
        settings.GARPIX_USER["PASSWORD_VALIDITY_PERIOD"] = 10
        settings.GARPIX_USER["PASSWORD_VALIDITY_INFORM_DAYS"] = 0
        user = self._create_user(11)

        SystemNotify.send = MagicMock()
        password_validity_passed()

        _msg = _('Your password has expired. Please change your password')

        SystemNotify.send.assert_called_once_with({
                "message": {
                    "message": str(_msg),
                },
                "event": settings.PASSWORD_INVALID_EVENT,
            }, user, event=settings.PASSWORD_INVALID_EVENT, room_name=f'workflow-{user.pk}',
        )

    def test_password_validity_passed(self) -> None:
        settings.GARPIX_USER["PASSWORD_VALIDITY_PERIOD"] = 10
        settings.GARPIX_USER["PASSWORD_VALIDITY_INFORM_DAYS"] = 3
        user = self._create_user(8)
        
        SystemNotify.send = MagicMock()
        password_validity_passed()

        expire_days=1
        _msg = _(
            'Your password will expire in {expire_days} {days}. Please change your password').format(
            expire_days=1 + expire_days,
            days=rupluralize(expire_days, _('day,days'))
        )

        SystemNotify.send.assert_called_once_with({
                "message": {
                    "message": str(_msg),
                },
                "event": settings.PASSWORD_INVALID_EVENT,
            }, user, event=settings.PASSWORD_INVALID_EVENT, room_name=f'workflow-{user.pk}',
        )

    def _create_user(self, password_update_days_old: int) -> User:
        return baker.make(
            User,
            username="test_user",
            password_updated_date=datetime.now() - timedelta(days=password_update_days_old),
            keycloak_auth_only=False,
        )
    
    def _delete_all_users(self) -> None:
        User.objects.all().delete()
