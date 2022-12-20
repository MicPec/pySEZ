from django.contrib import admin
from .models import Product, Unit


@admin.register(Product)
class ProductInfo(admin.ModelAdmin):
    list_display = ('name', 'unit', 'unit_price')

@admin.register(Unit)
class UnitInfo(admin.ModelAdmin):
    list_display = ('name', 'minvalue', 'maxvalue', 'step')
