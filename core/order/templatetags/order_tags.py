from django import template

register = template.Library()

@register.filter
def get_tax(total_price):
    return round(total_price * 0.09)
