from django.contrib import admin
from .models import Marker

@admin.register(Marker)
class StatusInfo(admin.ModelAdmin):
    list_display = ('id', 'name', 'color_code')