from django.contrib import admin
from solo.admin import SingletonModelAdmin
from ..models import GarpixUserConfig


@admin.register(GarpixUserConfig)
class GarpixUserConfigAdmin(SingletonModelAdmin):
    pass

