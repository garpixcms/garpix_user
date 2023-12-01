from garpix_utils.logs.enums.get_enums import Action
from garpix_utils.logs.loggers import ib_logger
from garpix_utils.logs.mixins.create_log import CreateLogMixin
from garpix_utils.models import AdminDeleteMixin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from garpix_user.utils.get_password_settings import get_password_settings


class UserAdmin(AdminDeleteMixin, BaseUserAdmin, CreateLogMixin):
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

    def delete_model(self, request, obj):
        action = Action.user_delete.value
        log = self.log_delete(ib_logger, request, obj, action)
        super().delete_model(request, obj)
        ib_logger.write_string(log)

    def delete_queryset(self, request, queryset):
        action = Action.user_delete.value
        logs = []
        for obj in queryset:
            logs.append(self.log_delete(ib_logger, request, obj, action))
        super().delete_queryset(request, queryset)
        for log in logs:
            ib_logger.write_string(log)

    def save_model(self, request, obj, form, change):
        password_first_change = get_password_settings()['password_first_change']

        if not change and password_first_change:
            obj.needs_password_update = True

        log = self.log_change_or_create(ib_logger, request, obj, change,
                                        action_change=Action.user_change.value,
                                        action_create=Action.user_create.value)
        ib_logger.write_string(log)
        super().save_model(request, obj, form, change)
