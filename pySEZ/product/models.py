from django.db import models


class Unit(models.Model):
    name = models.CharField(max_length=50)
    minvalue = models.DecimalField(
        max_digits=20, decimal_places=2, default=0, blank=True, null=True
    )
    maxvalue = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    step = models.DecimalField(
        max_digits=5, decimal_places=2, default=1, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(default=0.0, max_digits=20, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.unit_price}/{self.unit.name})"

    @property
    def orders_new(self):
        return self.orders.filter(status__state="NEW")

    @property
    def orders_pending(self):
        return self.orders.filter(status__state="PENDING")

    @property
    def orders_done(self):
        return self.orders.filter(status__state="DONE")
