from django.views.generic import View, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from shop.models import WishlistProductModel
from ...permissions import CustomerAccessPermission


class CustomerWishlistListView(LoginRequiredMixin, CustomerAccessPermission, ListView):
    template_name = 'dashboard/customer/wishlist/wishlist-list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = WishlistProductModel.objects.filter(user=self.request.user).select_related('product').prefetch_related('product__category')
        if q:= self.request.GET.get('q'):
            qs = qs.filter(product__title__icontains=q)
        return qs

class CustomerWishlistDeleteView(LoginRequiredMixin, CustomerAccessPermission, SuccessMessageMixin, DeleteView):
    http_method_names = ['post']
    success_url = reverse_lazy('dashboard:customer:wishlist-list')
    success_message = _('محصول با موفقیت از لیست علایق حذف شد')

    def get_queryset(self):
        return WishlistProductModel.objects.filter(user=self.request.user)
