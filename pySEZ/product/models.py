from django.db import models


class Unit(models.Model):
    db_column = 'unity'
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    unit_price = models.DecimalField(default=.0, max_digits=10, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.unit_price}/{self.unit.name})'
