from datetime import datetime, timedelta

from rest_framework.test import APITestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from model_bakery import baker

from garpix_user.tasks.delete_unconfirmed_users import delete_unconfirmed_users


class DeleteUnconfirmedUsersTest(APITestCase):
    def setUp(self) -> None:
        settings.GARPIX_USER["CONFIRMATION_DELAY"] = 10
        self.user_confirm = baker.make(
            get_user_model(),
            is_email_confirmed=True,
            is_phone_confirmed=True,
            username="confirmed_user",
        )
        self.user_unconfirm_email = baker.make(
            get_user_model(),
            is_email_confirmed=False,
            is_phone_confirmed=True,
        )
        self.user_unconfirm_phone = baker.make(
            get_user_model(),
            is_email_confirmed=True,
            is_phone_confirmed=False,
        )

    def test_delete_unconfirmed_users(self) -> None:
        self.user_unconfirm_email.date_joined = datetime.now() - timedelta(days=11)
        self.user_unconfirm_phone.date_joined = datetime.now() - timedelta(days=11)
        self.user_unconfirm_email.save()
        self.user_unconfirm_phone.save()
        delete_unconfirmed_users()
        self.assertEqual(len(get_user_model().objects.all()), 1)
        self.assertEqual(get_user_model().objects.all().first().username, self.user_confirm.username)
    
    def test_delete_unconfirmed_users_invalid(self) -> None:
        delete_unconfirmed_users()
        self.assertEqual(len(get_user_model().objects.all()), 3)

    def _delete_all_users(self) -> None:
        get_user_model().objects.all().delete()
