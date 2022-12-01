from django.forms import ModelForm
from .models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = (
            "lastname",
            "firstname",
            "company",
            "email",
            "phone",
            "website",
        )
