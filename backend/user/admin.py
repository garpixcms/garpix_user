from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    change_form_template = "send_confirm.html"
    fieldsets = (
                    ('Viber', {
                        'fields': (
                            'viber_chat_id',
                            'viber_secret_key',
                        )
                    }),
                    (None, {
                        'fields': ('phone', ),
                    }),
                    ('Telegram', {
                        'fields': ('telegram_chat_id', 'telegram_secret', 'get_telegram_connect_user_help'),
                    }),
                    ('Confim_information', {
                        'fields': ('is_phone_confirmed', 'phone_confirmation_code', 'new_phone'),
                    }),
                ) + UserAdmin.fieldsets
    readonly_fields = ['telegram_secret', 'get_telegram_connect_user_help'] + list(UserAdmin.readonly_fields)

    def response_change(self, request, obj):
        if (obj.new_email and "_send_confirm_code" in request.POST) or (obj.email and "_send_confirm_code" in request.POST):
            print('Тут должен отправиться код')
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)
