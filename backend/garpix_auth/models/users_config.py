from django.db import models
from solo.models import SingletonModel


class GarpixUserConfig(SingletonModel):

    class REGISTRATION_TYPE:
        """
        Настройки регистрации юзеров
        """

        NO_REGISTRATION = 0
        BEFORE_REGISTRATION = 1
        AFTER_REGISTRATION = 2

        TYPES = (
            (NO_REGISTRATION, 'Отключить подтверждение пользователя'),
            (BEFORE_REGISTRATION, 'Подтверждение пользователя до регистрации'),
            (AFTER_REGISTRATION, 'Подтверждение пользователя после регистрации'),
        )

    registration_type = models.IntegerField(default=REGISTRATION_TYPE.AFTER_REGISTRATION,
                                            choices=REGISTRATION_TYPE.TYPES,
                                            verbose_name='Тип подтверждения пользователя при регистрации')

    class Meta:
        verbose_name = 'Настройка регистрации'
        verbose_name_plural = 'Настройки регистрации'

