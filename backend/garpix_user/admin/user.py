from garpix_utils.models import AdminDeleteMixin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(AdminDeleteMixin, BaseUserAdmin):
    change_form_template = "garpix_user/send_confirm.html"

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_deleted', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Viber'), {
            'fields': ('viber_chat_id', 'viber_secret_key',)
        }),
        (_('Telegram'), {
            'fields': ('telegram_chat_id', 'telegram_secret', 'get_telegram_connect_user_help'),
        }),
        (_('Confim information'), {
            'fields': ('is_email_confirmed', 'email_confirmation_code', 'is_phone_confirmed', 'phone_confirmation_code'),
        }),
    )
    readonly_fields = ['telegram_secret', 'get_telegram_connect_user_help'] + list(BaseUserAdmin.readonly_fields)
