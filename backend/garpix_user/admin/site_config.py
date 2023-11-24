from django.contrib import admin
from garpix_utils.logs.mixins.log_admin_solo import LogAdminSolo
from solo.admin import SingletonModelAdmin
from garpix_user.models import GarpixUserPasswordConfiguration


@admin.register(GarpixUserPasswordConfiguration)
class GarpixUserPasswordConfigurationAdmin(LogAdminSolo, SingletonModelAdmin):
    pass
