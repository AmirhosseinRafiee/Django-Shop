from django.db.models import F, ExpressionWrapper, IntegerField, Value
from django.views.generic import ListView, DetailView
from .models import ProductModel, ProductStatus, ProductCategoryModel
from .filters import ProductFilter

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
        products_with_discounted_price = qs.annotate(
            discounted_price=discounted_price_expression
        )
        return ProductFilter(self.request.GET, products_with_discounted_price).qs


    def get_paginate_by(self, queryset):
        _paginate_by = self.request.GET.get('page_size', None)
        if _paginate_by in self.paginate_by_choices:
            return _paginate_by
        return self.paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_items'] = self.queryset.count()
        context['categories'] = ProductCategoryModel.objects.all()
        return context

class ShopProductDetailView(DetailView):
    template_name = 'shop/product-detail.html'
    queryset = ProductModel.objects.filter(status=ProductStatus.publish.value)
