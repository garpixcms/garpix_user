from django.contrib import admin
from garpix_user.models import UserSession


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    fields = ('user', 'token_number', 'recognized', 'last_access', 'is_phone_confirmed', 'is_email_confirmed')
