from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, ExpressionWrapper, IntegerField, Value, Count, Case, When, IntegerField, Exists, OuterRef, Prefetch, Subquery
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from review.models import ReviewProductModel, ReviewStatusType
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

    def get_queryset(self):
        accepted_reviews = ReviewProductModel.objects.filter(
            status=ReviewStatusType.accepted.value
        ).select_related('user__profile')

        rating_counts = accepted_reviews.values('product_id').annotate(
            one_star=Count(Case(When(rate=1, then=1),
                                output_field=IntegerField())),
            two_star=Count(Case(When(rate=2, then=1),
                                output_field=IntegerField())),
            three_star=Count(Case(When(rate=3, then=1),
                                  output_field=IntegerField())),
            four_star=Count(Case(When(rate=4, then=1),
                                 output_field=IntegerField())),
            five_star=Count(Case(When(rate=5, then=1),
                                 output_field=IntegerField())),
        )

        qs = ProductModel.objects.all().prefetch_related(
            'productimagemodel_set',
            Prefetch('reviewproductmodel_set', queryset=accepted_reviews)
        ).annotate(
            one_star_reviews=Subquery(
                rating_counts.filter(
                    product_id=OuterRef('pk')).values('one_star'),
                output_field=IntegerField()
            ),
            two_star_reviews=Subquery(
                rating_counts.filter(
                    product_id=OuterRef('pk')).values('two_star'),
                output_field=IntegerField()
            ),
            three_star_reviews=Subquery(
                rating_counts.filter(product_id=OuterRef(
                    'pk')).values('three_star'),
                output_field=IntegerField()
            ),
            four_star_reviews=Subquery(
                rating_counts.filter(
                    product_id=OuterRef('pk')).values('four_star'),
                output_field=IntegerField()
            ),
            five_star_reviews=Subquery(
                rating_counts.filter(
                    product_id=OuterRef('pk')).values('five_star'),
                output_field=IntegerField()
            ),
        )

        if self.request.user.is_authenticated:
            wishlist_subquery = WishlistProductModel.objects.filter(
                user=self.request.user,
                product=OuterRef('pk')
            )
            qs = qs.annotate(
                in_wishlist=Exists(wishlist_subquery)
            )
        return qs


class WishlistToggleView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(ProductModel, id=product_id)
        wishlist, created = WishlistProductModel.objects.get_or_create(
            user=self.request.user, product=product)
        if not created:
            wishlist.delete()
            status, message = 204, _('محصول با موفقیت از لیست علایق حذف شد')
        else:
            status, message = 201, _('محصول با موفقیت به لیست علایق اضافه شد')

        return JsonResponse({'message': message}, status=status)
