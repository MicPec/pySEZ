from django_filters import FilterSet

from order.models import Order


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            "id": ["exact"],
            "user": ["exact"],
            "client": ["exact"],
            "date_created": ["exact", "gt"],
            "products": ["exact"],
            "status": ["exact"],
        }
