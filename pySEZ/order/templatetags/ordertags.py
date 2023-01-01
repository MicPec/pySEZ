from django import template

register = template.Library()


@register.simple_tag
def orderitem(order, product):
    return order.orderitem_set.get(product=product).pk


@register.simple_tag
def product_qty(order, product):
    return order.orderitem_set.get(product=product).quantity


@register.simple_tag
def product_note(order, product):
    return order.orderitem_set.get(product=product).note


@register.simple_tag
def product_amount_price(order, product):
    return round(order.orderitem_set.get(product=product).amount, 2)
