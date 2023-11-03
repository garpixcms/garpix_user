from django.contrib import admin
from solo.admin import SingletonModelAdmin
from garpix_user.models import GarpixUserPasswordConfiguration


@admin.register(GarpixUserPasswordConfiguration)
class GarpixUserPasswordConfigurationAdmin(SingletonModelAdmin):
    pass
