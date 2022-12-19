import django_filters as DF
from django_filters.widgets import DateRangeWidget
from crispy_forms.bootstrap import AppendedText, FormActions, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Button, Column, Div, Field, Layout, Row, Submit
from django import forms
from order.models import Order


class OrderFilter(DF.FilterSet):
    date_created = DF.DateFromToRangeFilter(
        field_name="date_created",
        label="Date created",
        widget=DateRangeWidget(
            attrs={
                "class": "form-control",
                "type": "date",
                # "template_name": "/templates/scraps/_daterangepicker.html",
            },
        ),
    )
    deadline = DF.DateFromToRangeFilter(
        field_name="deadline",
        label="Deadline",
        widget=DateRangeWidget(attrs={"class": "form-control", "type": "date"}),
    )
    date_finished = DF.DateFromToRangeFilter(
        field_name="date_finished",
        label="Date finished",
        widget=DateRangeWidget(attrs={"class": "form-control", "type": "date"}),
    )

    class Meta:
        model = Order
        fields = {
            "id": ["exact"],
            "user": ["exact"],
            "client": ["exact"],
            # "date_created": ["gte", "lte"],
            # "date_finished": ["gte", "lte"],
            # "deadline": ["lte", "gte"],
            "products": ["exact"],
            "status": ["exact"],
            "status__state": ["exact"],
            "note": ["icontains"],
        }
