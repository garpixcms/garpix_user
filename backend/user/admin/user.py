from django.contrib import admin

from user.models import User
from garpix_user.models import UserSession
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    change_form_template = "send_confirm.html"
    fieldsets = (
                    ('Viber', {
                        'fields': (
                            'viber_chat_id',
                            'viber_secret_key',
                        )
                    }),
                    (None, {
                        'fields': ('phone',),
                    }),
                    ('Telegram', {
                        'fields': ('telegram_chat_id', 'telegram_secret', 'get_telegram_connect_user_help'),
                    }),
                    ('Confim_information', {
                        'fields': ('is_email_confirmed', 'email_confirmation_code', 'new_email'),
                    }),
                ) + UserAdmin.fieldsets
    readonly_fields = ['telegram_secret', 'get_telegram_connect_user_help'] + list(UserAdmin.readonly_fields)


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    pass
