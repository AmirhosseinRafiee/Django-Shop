from django.views.generic import ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from shop.models import ProductCategoryModel, FeaturedProductModel
from ..forms import AdminFeaturedProductForm
from ...permissions import AdminAccessPermission


class AdminFeaturedProductListView(LoginRequiredMixin, AdminAccessPermission, ListView):
    template_name = 'dashboard/admin/featured-product/featured-product-list.html'
    queryset = FeaturedProductModel.objects.all().select_related(
        'product').prefetch_related('product__category')
    extra_context = {'categories': ProductCategoryModel.objects.all()}
    paginate_by = 10


class AdminFeaturedProductCreateView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, CreateView):
    http_method_names = ["post", "options"]
    form_class = AdminFeaturedProductForm
    success_message = _('با موفقیت به محصولات ویژه اضافه شد')

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.request.META.get('HTTP_REFERER'))

    def get_success_url(self):
        return reverse('dashboard:admin:product-edit', kwargs={'pk': self.object.product.id})


class AdminFeaturedProductDeleteView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, DeleteView):
    http_method_names = ["post", "options"]
    model = FeaturedProductModel
    success_url = reverse_lazy('dashboard:admin:featured-product-list')
    success_message = _('با موفقیت از محصولات ویژه حذف شد')

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.request.META.get('HTTP_REFERER'))
