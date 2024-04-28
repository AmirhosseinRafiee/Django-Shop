from django.forms import BaseForm
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Count, ProtectedError
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from order.models import CuponModel
from ...permissions import AdminAccessPermission
from ..filters import AdminCouponFilter
from ..forms import AdminCouponForm


class AdminCouponListView(LoginRequiredMixin, AdminAccessPermission, ListView):
    template_name = 'dashboard/admin/coupon/coupon-list.html'
    queryset = CuponModel.objects.all()
    queryset = coupon_queryset = CuponModel.objects.annotate(num_users_used=Count('used_by')).values(
        'id', 'code', 'discount_percent', 'max_discount_amount', 'max_limit_usage', 'num_users_used', 'expiration_date')
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        qs = super().get_queryset()
        return AdminCouponFilter(self.request.GET, qs).qs

class AdminCouponCreateView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, CreateView):
    template_name = 'dashboard/admin/coupon/coupon-create.html'
    form_class = AdminCouponForm
    success_message = _('ایجاد تخفیف با موفقیت انجام شد')

    def get_success_url(self):
        return reverse('dashboard:admin:coupon-edit', kwargs={'pk': self.object.pk})

class AdminCouponEditView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/coupon/coupon-edit.html'
    model = CuponModel
    form_class = AdminCouponForm
    success_url = reverse_lazy('dashboard:admin:coupon-list')
    success_message = _('بروزرسانی تخفیف با موفقیت انجام شد')


class AdminCouponDeleteView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, DeleteView):
    template_name = 'dashboard/admin/coupon/coupon-delete.html'
    model = CuponModel
    success_url = reverse_lazy('dashboard:admin:coupon-list')
    success_message = _('حذف تخفیف با موفقیت انجام شد')

    def form_valid(self, form):
        try:
            self.object.delete()
        except ProtectedError:
            messages.error(self.request, _("این کوپن نمی‌تواند حذف شود زیرا با سفارش‌های موجود مرتبط است."))
            return redirect(reverse('dashboard:admin:coupon-edit', kwargs={'pk': self.object.pk}))
        success_url = self.get_success_url()
        return redirect(success_url)
