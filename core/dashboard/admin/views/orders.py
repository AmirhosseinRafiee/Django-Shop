from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from order.models import OrderModel, OrderStatusType
from ..filters import AdminOrderFilter
from ...permissions import AdminAccessPermission


class AdminOrderListView(LoginRequiredMixin, AdminAccessPermission, ListView):
    template_name = 'dashboard/admin/order/order-list.html'
    queryset = OrderModel.objects.select_related('user__profile')
    extra_context = {'status_types': OrderStatusType.choices}
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        qs = super().get_queryset()
        return AdminOrderFilter(self.request.GET, qs).qs


class AdminOrderEditView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/order/order-detail.html'
    extra_context = {'status_types': OrderStatusType.choices}
    queryset = OrderModel.objects.prefetch_related(
        'orderitemmodel_set__product')
    fields = ['status']
    success_message = _('سفارش با موفقیت ویرایش شد')

    def get_success_url(self):
        return reverse('dashboard:admin:order-edit', kwargs={'pk': self.object.pk})
