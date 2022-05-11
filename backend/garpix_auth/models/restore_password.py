from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from garpix_notify.models import Notify
from garpix_utils.string import get_random_string

import string
from datetime import datetime, timezone, timedelta


class RestorePasswordMixin(models.Model):

    restore_password_confirm_code = models.CharField(
        max_length=15, verbose_name='Код сброса пароля по почте', null=True, blank=True)
    is_restore_code_confirmed = models.BooleanField(default=False, verbose_name="Код посстановления подтвержден")
    restore_token = models.CharField(max_length=40, verbose_name="Токен восстановления пароля", default='')
    restore_date = models.DateTimeField(null=True, verbose_name="Дата отправки кода восстановления")

    class Meta:
        abstract = True

    @classmethod
    def send_restore_code(cls, email=None, phone=None, user=None):

        confirmation_code = get_random_string(settings.GARPIX_CONFIRM_CODE_LENGTH, string.digits)
        if email:
            user = cls.objects.filter(email=email, is_email_confirmed=True).first()
        elif phone:
            user = cls.objects.filter(phone=phone, is_email_confirmed=True).first()
        if not user:
            return {"result": False, "message": "Пользователь не зарегистрирован"}
        if user.restore_date and user.restore_date + timedelta(
                minutes=settings.GARPIX_TIME_LAST_REQUEST) > datetime.now(user.restore_date.tzinfo):
            return {"result": False,
                    "message": f"Не прошло {settings.GARPIX_TIME_LAST_REQUEST} мин с последней отправки"}

        user.restore_password_confirm_code = confirmation_code
        user.restore_date = datetime.now(timezone.utc)
        user.save()

        if email:
            Notify.send(settings.EMAIL_RESTORE_PASSWORD_EVENT, {
                'user_fullname': str(user),
                'email': user.email,
                'restore_key': user.restore_password_confirm_code
            }, email=user.email)
        elif phone:
            Notify.send(settings.EMAIL_RESTORE_PASSWORD_EVENT, {
                'user_fullname': str(user),
                'phone': user.phone,
                'restore_key': user.restore_password_confirm_code
            }, phone=user.phone)

        return {"result": True}

    @classmethod
    def check_restore_code(cls, email=None, phone=None, confirmation_code=None, user=None):
        if email:
            user = cls.objects.filter(email=email, restore_password_confirm_code=confirmation_code).first()
        elif phone:
            user = cls.objects.filter(phone=phone, restore_password_confirm_code=confirmation_code).first()
        if not user:
            return {"result": False, "message": "Данные пользователя или код введены неверно"}

        time_is_up = (datetime.now(
            user.restore_date.tzinfo) - user.restore_date).seconds / 60 > settings.GARPIX_CONFIRM_EMAIL_CODE_LIFE_TIME

        if time_is_up:
            return {"result": False, "message": "Код недействителен. Запросите повторно"}

        user.restore_token = uuid4()
        user.is_restore_code_confirmed = True
        user.save()

        return {"result": True, "token": user.restore_token}

    @classmethod
    def restore_password(cls, email=None, phone=None, token=None, new_password=None, user=None):
        if email:
            user = cls.objects.filter(email=email, is_restore_code_confirmed=True, restore_token=token).first()
        elif phone:
            user = cls.objects.filter(phone=phone, is_restore_code_confirmed=True, restore_token=token).first()
        if not user:
            return {"result": False, "message": "Данные пользоваетля не подтверждены"}
        user.set_password(new_password)
        user.save()
        return {"result": True, "message": "Пароль был успешно изменен"}
