from django.contrib import admin

from ..models.refferal import ReferralType


@admin.register(ReferralType)
class ReferralTypeAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title']
