from django.forms import ModelForm
from django import forms

from product.models import Product
from .models import Order, OrderItem


class OrderItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)

    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
            "note",
        )

        widgets = {
            "quantity": forms.NumberInput(
                attrs={"type": "number", "min": 0, "step": 0.01}
            ),
            "note": forms.Textarea(attrs={"rows": 3}),
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        # products = OrderItemFormSet

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
    comment = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Order
        fields = ("status", "comment")
