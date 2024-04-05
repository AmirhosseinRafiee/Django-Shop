from django import template
from ..models import ProductModel, ProductStatus

register = template.Library()


@register.inclusion_tag('includes/latest-products.html')
def latest_products():
    products = ProductModel.objects.filter(
        status=ProductStatus.publish.value).prefetch_related('category').order_by('-created_date')[:8]
    return {'products': products}


@register.inclusion_tag('includes/similar-products.html')
def similar_products(product: ProductModel):
    products = ProductModel.objects.filter(
        status=ProductStatus.publish.value,
        category__in=product.category.all()
    ).exclude(id=product.id).prefetch_related('category').order_by('-created_date')[:4]
    return {'similar_products': products}

