from django.db.models import F, ExpressionWrapper, IntegerField, Value
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from shop.models import ProductModel, ProductCategoryModel
from ..forms import AdminProductEditForm
from ..filters import AdminProductFilter
from ...permissions import AdminAccessPermission

class AdminProductListView(LoginRequiredMixin, AdminAccessPermission, ListView):
    template_name = 'dashboard/admin/product/product-list.html'
    queryset = ProductModel.objects.all()
    extra_context = {'categories': ProductCategoryModel.objects.all()}
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('category')
        return AdminProductFilter(self.request.GET, qs).qs

class AdminProductEditView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/product/product-edit.html'
    queryset = ProductModel.objects.all()
    form_class = AdminProductEditForm
    extra_context = {'categories': ProductCategoryModel.objects.all()}
    success_url = reverse_lazy('dashboard:admin:product-list')
    success_message = _('بروزرسانی محصول با موفقیت انجام شد')
