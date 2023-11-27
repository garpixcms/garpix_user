from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from garpix_utils.logs.mixins.log_admin import LogAdminMixin


admin.site.unregister(Group)


@admin.register(Group)
class GarpixGroupAdmin(LogAdminMixin, GroupAdmin):
    pass
