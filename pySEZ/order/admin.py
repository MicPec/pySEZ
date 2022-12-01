from django.contrib import admin
from .models import Order, OrderItem, Product


class ItemInfoInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderInfo(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'deadline', 'client', 'get_products','status')
    inlines = [ItemInfoInline]
    filter_horizontal = ('markers', 'products',)
