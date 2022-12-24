from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import Order, OrderItem


class OrderProductForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
            "note",
        )

        widgets = {
            "note": forms.Textarea(attrs={"rows": 3}),
            "quantity": forms.NumberInput(attrs={"type": "number", "step": 0.01}),
        }

OrderProductFormSet = inlineformset_factory(
    Order, OrderItem, form=OrderProductForm, extra=1, can_delete=True
)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        products = OrderProductFormSet

        fields = (
            "client",
            "deadline",
            "discount",
            "note",
        )

        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "note": forms.Textarea(attrs={"rows": 3}),
            "discount": forms.NumberInput(
                attrs={"type": "number", "min": -100, "max": 999, "step": 0.01}
            ),
        }


class OrderStatusUpdate(ModelForm):
    class Meta:
        model = Order
        fields = ("status",)
