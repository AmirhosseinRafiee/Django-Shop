from django.db.models import F, ExpressionWrapper, IntegerField, Value
from django.views.generic import ListView
from shop.models import ProductModel, ProductCategoryModel
from ..filters import AdminProductFilter

class AdminProductListView(ListView):
    template_name = 'dashboard/admin/product/product-list.html'
    queryset = ProductModel.objects.all()
    extra_context = {'categories': ProductCategoryModel.objects.all()}
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('category')
        discounted_price_expression = ExpressionWrapper(
            F('price') - (F('price') * F('discount_percent') / Value(100)),
            output_field=IntegerField()
        )
        products_with_discounted_price = qs.annotate(
            discounted_price=discounted_price_expression
        )
        return AdminProductFilter(self.request.GET, products_with_discounted_price).qs

