from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from garpix_utils.cef_logs.mixins.create_log import CreateLogMixin

admin.site.unregister(Group)


@admin.register(Group)
class GarpixGroupAdmin(CreateLogMixin, GroupAdmin):

    def save_model(self, request, obj, form, change):
        events = self.logs_change_or_create(request, obj, change)
        super().save_model(request, obj, form, change)
        for event, params in events:
            event(**params)

    def save_related(self, request, form, formsets, change):
        if change:
            events = self.logs_change_m2m_field(request, super(), form, formsets, change)
            for event, params in events:
                event(**params)
        else:
            super().save_related(request, form, formsets, change)

    def delete_model(self, request, obj):
        event, params = self.log_delete(request, obj)
        super().delete_model(request, obj)
        event(**params)

    def delete_queryset(self, request, queryset):
        events = []
        for obj in queryset:
            events.append(self.log_delete(request, obj))
        super().delete_queryset(request, queryset)
        for event, params in events:
            event(**params)
