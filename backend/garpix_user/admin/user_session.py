from django.contrib import admin
from ..models import UserSession


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    pass
