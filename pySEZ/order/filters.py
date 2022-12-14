from django_filters import FilterSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Column
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from order.models import Order


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            "id": ["exact"],
            "user": ["exact"],
            "client": ["exact"],
            "date_created": ["gte", "lte"],
            "date_finished": ["gte", "lte"],
            "deadline": ["gte", "lte"],
            "products": ["exact"],
            "status": ["exact"],
            "status__state": ["exact"],
        }
