from django.contrib import admin
from garpix_utils.logs.mixins.log_admin import LogAdminMixin

from ..models import PasswordHistory


@admin.register(PasswordHistory)
class PasswordHistoryAdmin(LogAdminMixin):
    list_display = ['user', 'created_at']

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False
