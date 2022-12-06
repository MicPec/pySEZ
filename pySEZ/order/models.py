from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin
from django.contrib.auth.models import User
from client.models import Client
from status.models import Status
from marker.models import Marker
from product.models import Product
from pySEZ.utils import get_sentinel_user


class Order(models.Model):
    client = models.ForeignKey(Client, related_name="orders", on_delete=models.RESTRICT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True)
    dsc_price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[
            MinValueValidator(0.0),
        ],
        blank=True,
        null=True,
    )
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, related_name="orders", through="OrderItem"
    )
    markers = models.ManyToManyField(Marker, related_name="markers", blank=True)

    # status_log = models.ForeignKey(StatusLog, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.client} | "
            f'Data: {self.date_created.strftime("%Y-%m-%d") } | '
            f"Status: {self.status} | "
            f'Produkty: {", ".join([p.name for p in self.products.all()])}'
        )

    @property
    def total_amount(self):
        return sum(
            oi.amount for oi in self.orderitem_set.all()
        )

    @admin.display
    def get_products(self):
        return ", ".join([p.name for p in self.products.all()])


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.DecimalField(default=1.0, max_digits=10, decimal_places=2)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product.name} - ({self.quantity} {self.product.unit.name})"

    def get_absolute_url(self):
        return redirect("order-detail", pk=self.pk)

    @property
    def amount(self):
        return self.quantity * self.product.unit_price
