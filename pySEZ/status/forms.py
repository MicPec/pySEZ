from django.forms import ModelForm, TextInput

from .models import Status


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = "__all__"
        widgets = {"color": TextInput(attrs={"type": "color"})}
