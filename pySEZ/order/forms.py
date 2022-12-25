from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import Order, OrderItem


# class OrderProductForm(ModelForm):
#     class Meta:
#         model = OrderItem
#         fields = (
#             "product",
#             "quantity",
#             "note",
#         )

#         widgets = {
#             "note": forms.Textarea(attrs={"rows": 3}),
#             "quantity": forms.NumberInput(attrs={"type": "number", "step": 0.01}),
#         }

class OrderItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.model = OrderItem
        self.fields['quantity'].widget.attrs.update(
            {'min': self.get_object().product.unit.minvalue,
             'max': self.get_object().product.unit.maxvalue,
             'step': self.get_object().product.unit.step})

    def get_object(self):
        obj = self.model.objects.get(pk=self.instance.pk)
        return obj
    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
            "note",
        )

        widgets = {
            "quantity": forms.NumberInput(attrs={"type": "number", "step": 0.01}),
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
    class Meta:
        model = Order
        fields = ("status",)
