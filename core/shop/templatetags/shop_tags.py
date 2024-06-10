from django import template
from django.db.models import Q, OuterRef, Count, Exists
from ..models import ProductModel, ProductStatus, WishlistProductModel, FeaturedProductModel

register = template.Library()


@register.inclusion_tag('includes/latest-products.html', takes_context=True)
def latest_products(context):
    request = context.get('request')
    products = ProductModel.objects.filter(
        status=ProductStatus.publish.value).prefetch_related('category').order_by('-created_date')[:8]
    if request.user.is_authenticated:
        wishlist_subquery = WishlistProductModel.objects.filter(
            user=request.user,
            product=OuterRef('pk')
        )
        products = products.annotate(
            in_wishlist=Exists(wishlist_subquery)
        )
    return {'products': products, 'request': request}


@register.inclusion_tag('includes/similar-products.html', takes_context=True)
def similar_products(context):
    request = context.get('request')
    product = context.get('object')
    shared_category_count = Count('category', filter=Q(
        category__in=product.category.all()))
    products = ProductModel.objects.filter(
        status=ProductStatus.publish.value,
    ).exclude(id=product.id).annotate(
        shared_category_count=shared_category_count
    ).prefetch_related('category').order_by('-shared_category_count', '-created_date').distinct()[:4]
    if request.user.is_authenticated:
        wishlist_subquery = WishlistProductModel.objects.filter(
            user=request.user,
            product=OuterRef('pk')
        )
        products = products.annotate(
            in_wishlist=Exists(wishlist_subquery)
        )
    return {'similar_products': products, 'request': request}


@register.inclusion_tag('includes/featured-products.html')
def featured_products():
    featured_products = FeaturedProductModel.objects.select_related(
        'product').filter(product__status=ProductStatus.publish.value)
    return {'featured_products': featured_products}
