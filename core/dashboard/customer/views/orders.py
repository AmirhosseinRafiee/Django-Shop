from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from order.models import OrderModel
from order.permissions import IsOrderDeliveredMixin
from ...permissions import CustomerAccessPermission


class CustomerOrderListView(LoginRequiredMixin, CustomerAccessPermission, ListView):
    template_name = 'dashboard/customer/order/order-list.html'
    paginate_by = 5

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        qs = OrderModel.objects.filter(user=self.request.user).prefetch_related(
            'orderitemmodel_set__product')
        search = self.request.GET.get('s')
        if search:
            if search.isdigit():
                qs = qs.filter(id=search)
            else:
                qs = qs.filter(orderitemmodel__product__title__contains=search)
        return qs


class CustomerOrderEditView(LoginRequiredMixin, CustomerAccessPermission, DetailView):
    template_name = 'dashboard/customer/order/order-detail.html'

    def get_queryset(self):
        return OrderModel.objects.filter(
            user=self.request.user
        ).prefetch_related(
            'orderitemmodel_set__product'
        )


class CustomerOrderInvoiceView(LoginRequiredMixin, CustomerAccessPermission, IsOrderDeliveredMixin, DetailView):
    template_name = 'dashboard/customer/order/order-invoice.html'

    def get_queryset(self):
        return OrderModel.objects.filter(
            user=self.request.user
        ).select_related(
            'user__profile'
        ).prefetch_related(
            'orderitemmodel_set__product'
        )
