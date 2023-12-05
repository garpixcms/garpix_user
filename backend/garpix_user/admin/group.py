from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from garpix_utils.logs.enums.get_enums import Action
from garpix_utils.logs.loggers import ib_logger
from garpix_utils.logs.mixins.create_log import CreateLogMixin

admin.site.unregister(Group)


@admin.register(Group)
class GarpixGroupAdmin(CreateLogMixin, GroupAdmin):

    def save_model(self, request, obj, form, change):
        log = self.log_change_or_create(ib_logger, request, obj, change,
                                        action_change=Action.group_change.value,
                                        action_create=Action.group_create.value)
        super().save_model(request, obj, form, change)
        ib_logger.write_string(log)

    def save_related(self, request, form, formsets, change):
        if change:
            log = self.log_change_m2m_field(ib_logger, request, super(), form, formsets, change,
                                            action_change=Action.group_change.value,)
            ib_logger.write_string(log)
        else:
            super().save_related(request, form, formsets, change)

    def delete_model(self, request, obj):
        action = Action.group_delete.value
        log = self.log_delete(ib_logger, request, obj, action)
        super().delete_model(request, obj)
        ib_logger.write_string(log)

    def delete_queryset(self, request, queryset):
        action = Action.group_delete.value
        logs = []
        for obj in queryset:
            logs.append(self.log_delete(ib_logger, request, obj, action))
        super().delete_queryset(request, queryset)
        for log in logs:
            ib_logger.write_string(log)
