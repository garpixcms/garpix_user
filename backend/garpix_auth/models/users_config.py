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
    min_length_password = models.IntegerField(default=8, verbose_name='Минимальная длина пароля')
    min_digits_password = models.IntegerField(default=2, verbose_name='Минимальное количество цифр в пароле')
    min_chars_password = models.IntegerField(default=2, verbose_name='Минимальное количество букв в пароле')
    min_uppercase_password = models.IntegerField(default=1, verbose_name='Минимальное количество заглавных букв в пароле')

    class Meta:
        verbose_name = 'Настройка регистрации'
        verbose_name_plural = 'Настройки регистрации'

