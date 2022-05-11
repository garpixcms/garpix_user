from django.contrib import admin
from solo.admin import SingletonModelAdmin
from ..models import GarpixUserConfig


@admin.register(GarpixUserConfig)
class GarpixUserConfigAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Сложность пароля при регистрации', {
            'fields': (
                'min_length_password',
                'min_digits_password',
                'min_chars_password',
                'min_uppercase_password',

            )
        }),)

