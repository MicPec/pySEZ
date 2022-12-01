from django.contrib import admin
from .models import Status

@admin.register(Status)
class StatusInfo(admin.ModelAdmin):
    list_display = ('name', 'color_code', 'state')
