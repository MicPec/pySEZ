from django import template

register = template.Library()


@register.simple_tag
def product_qty(order, product):
    return order.orderitem_set.get(product=product).quantity


@register.simple_tag
def product_note(order, product):
    return order.orderitem_set.get(product=product).note
