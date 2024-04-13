from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from shop.models import ProductModel, ProductCategoryModel
from ..forms import AdminProductForm
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

class AdminProductCreateView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, CreateView):
    template_name = 'dashboard/admin/product/product-create.html'
    form_class = AdminProductForm
    extra_context = {'categories': ProductCategoryModel.objects.all()}
    success_message = _('ایجاد محصول با موفقیت انجام شد')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('dashboard:admin:product-edit', kwargs={'pk': self.object.pk})

class AdminProductEditView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/product/product-edit.html'
    queryset = ProductModel.objects.all()
    form_class = AdminProductForm
    extra_context = {'categories': ProductCategoryModel.objects.all()}
    success_url = reverse_lazy('dashboard:admin:product-list')
    success_message = _('بروزرسانی محصول با موفقیت انجام شد')

class AdminProductDeleteView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, DeleteView):
    template_name = 'dashboard/admin/product/product-delete.html'
    queryset = ProductModel.objects.all()
    success_url = reverse_lazy('dashboard:admin:product-list')
    success_message = _('حذف محصول با موفقیت انجام شد')
