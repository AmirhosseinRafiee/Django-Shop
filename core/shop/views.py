from typing import Any
from django.db.models import F, ExpressionWrapper, IntegerField, Value
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from django.db.models import Exists, OuterRef
from .models import ProductModel, ProductStatus, ProductCategoryModel, WishlistProductModel
from .filters import ProductFilter
from .permissons import IsAdminOrPublishedPermission

class ShopProductGridView(ListView):
    template_name = 'shop/product-grid.html'
    queryset = ProductModel.objects.filter(status=ProductStatus.publish.value)
    paginate_by = 9
    paginate_by_choices = ['9', '18', '27']

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('category')
        discounted_price_expression = ExpressionWrapper(
            F('price') - (F('price') * F('discount_percent') / Value(100)),
            output_field=IntegerField()
        )
        qs = qs.annotate(
            discounted_price=discounted_price_expression
        )

        if self.request.user.is_authenticated:
            # Subquery to check if the product is in the user's wishlist
            wishlist_subquery = WishlistProductModel.objects.filter(
                user=self.request.user,
                product=OuterRef('pk')
            )

            # Annotate the products with the existence of the product in the wishlist
            qs = qs.annotate(
                in_wishlist=Exists(wishlist_subquery)
            )

        return ProductFilter(self.request.GET, qs).qs


    def get_paginate_by(self, queryset):
        _paginate_by = self.request.GET.get('page_size', None)
        if _paginate_by in self.paginate_by_choices:
            return _paginate_by
        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategoryModel.objects.all()
        return context

class ShopProductDetailView(IsAdminOrPublishedPermission, DetailView):
    template_name = 'shop/product-detail.html'
    queryset = ProductModel.objects.all().prefetch_related('productimagemodel_set')

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            wishlist_subquery = WishlistProductModel.objects.filter(
                user=self.request.user,
                product=OuterRef('pk')
            )
            qs = qs.annotate(
                in_wishlist=Exists(wishlist_subquery)
            )
        return qs
