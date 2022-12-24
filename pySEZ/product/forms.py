from django.forms import ModelForm
from django import forms
from .models import Product, Unit


class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ("name", "minvalue", "maxvalue", "step")


class ProductForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(ModelForm, self).__init__(*args, **kwargs)
    #     self.model = Product
    #     self.fields['unit_price'].widget.attrs.update(
    #         {'min': self.get_object().unit.minvalue,
    #          'max': self.get_object().unit.maxvalue,
    #          'step': self.get_object().unit.step})

    # def get_object(self):
    #     obj = self.model.objects.get(pk=self.instance.pk)
    #     return obj


    class Meta:
        model=Product
        fields = ("name", "unit",  "unit_price",)
