from django.db import models
from solo.models import SingletonModel


class GarpixUserConfig(SingletonModel):
    """Настройки регистрации юзеров"""
    min_length_password = models.IntegerField(default=8, verbose_name='Минимальная длина пароля')
    min_digits_password = models.IntegerField(default=2, verbose_name='Минимальное количество цифр в пароле')
    min_chars_password = models.IntegerField(default=2, verbose_name='Минимальное количество букв в пароле')
    min_uppercase_password = models.IntegerField(default=1,
                                                 verbose_name='Минимальное количество заглавных букв в пароле')

    class Meta:
        verbose_name = 'Настройка регистрации'
        verbose_name_plural = 'Настройки регистрации'

    def __str__(self):
        return 'Настройки регистрации'

