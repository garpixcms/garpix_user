from garpix_utils.models import AdminDeleteMixin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from garpix_user.utils.get_password_settings import get_password_settings


class UserAdmin(AdminDeleteMixin, BaseUserAdmin):
    change_form_template = "garpix_user/send_confirm.html"

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_deleted', 'is_staff', 'is_superuser',
                'is_blocked', 'login_attempts_count', 'password_updated_date', 'needs_password_update',
                'groups', 'user_permissions', 'keycloak_auth_only'
            ),
        }),
        (_('Viber'), {
            'fields': ('viber_chat_id', 'viber_secret_key',)
        }),
        (_('Telegram'), {
            'fields': ('telegram_chat_id', 'telegram_secret', 'get_telegram_connect_user_help'),
        }),
        (_('Confim information'), {
            'fields': (
                'is_email_confirmed', 'email_confirmation_code', 'is_phone_confirmed', 'phone_confirmation_code'),
        }),
    )
    readonly_fields = ['telegram_secret', 'get_telegram_connect_user_help'] + list(BaseUserAdmin.readonly_fields)

    def save_model(self, request, obj, form, change):
        password_first_change = get_password_settings()['password_first_change']

        if not change and password_first_change:
            obj.needs_password_update = True

        super().save_model(request, obj, form, change)
