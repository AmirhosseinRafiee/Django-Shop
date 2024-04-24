from django import template

register = template.Library()

@register.filter
def get_products_quantity_in_cart(cart, product_id):
    return cart.get_product_quantity(str(product_id))
