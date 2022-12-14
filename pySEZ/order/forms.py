from django.forms import ModelForm
from django import forms
from .models import Order


class OrderForm(ModelForm):
    deadline = forms.DateInput()

    class Meta:
        model = Order
        fields = (
            "client",
            "deadline",
            "note",
            "discount",
            "products",
        )

class OrderStatusUpdate(ModelForm):

    class Meta:
        model = Order
        fields = (
            "status",
        )