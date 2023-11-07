from solo.models import SingletonModel
from django.db import models
from django.utils.translation import gettext as _


class GarpixUserPasswordConfiguration(SingletonModel):
    min_length = models.PositiveIntegerField(default=12, verbose_name=_('Минимальная длина пароля'))
    min_digits = models.PositiveIntegerField(default=2, verbose_name=_('Минимальное количество цифр'))
    min_chars = models.PositiveIntegerField(default=2, verbose_name=_('Минимальное количество букв'))
    min_uppercase = models.PositiveIntegerField(default=1, verbose_name=_('Минимальное количество заглавных букв'))
    min_special_symbols = models.PositiveIntegerField(default=1, verbose_name=_('Минимальное количество спец.символов'))
    available_attempt = models.IntegerField(default=-1, help_text=_('-1 если ограничение не требуется'),
                                            verbose_name=_('Количество допустимых неуспешных попыток входа'))
    password_history = models.IntegerField(default=-1, help_text=_('-1 если ограничение не требуется'),
                                           verbose_name=_(
                                               'Количество последних паролей, которые нельзя использовать при смене'))
    password_validity_period = models.IntegerField(default=-1, help_text=_('-1 если ограничение не требуется'),
                                                   verbose_name=_(
                                                       'Срок действия пароля (в днях)')
                                                   )
    password_first_change = models.BooleanField(default=False, verbose_name=_('Обязательная смена пароля при первом входе'))

    class Meta:
        verbose_name = 'Настройки безопасности входа'
        verbose_name_plural = 'Настройки безопасности входа'

    def __str__(self):
        return ''
