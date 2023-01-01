from django.contrib import admin
from django.forms import TextInput

from .forms import StatusForm

from .models import Status


@admin.register(Status)
class StatusInfo(admin.ModelAdmin):
    form = StatusForm
