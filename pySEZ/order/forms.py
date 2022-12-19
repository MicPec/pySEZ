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

        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 2}),
            "discount": forms.NumberInput(
                attrs={"type": "number", "min": -100, "max": 999, "step": 0.01}
            ),
        }


class OrderStatusUpdate(ModelForm):
    class Meta:
        model = Order
        fields = ("status",)
