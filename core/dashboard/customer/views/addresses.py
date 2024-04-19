from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from order.models import UserAddressModel
from ...permissions import CustomerAccessPermission
from ..forms import CustumerAddressCreateFrom

class CustomerAddressListView(LoginRequiredMixin, CustomerAccessPermission, ListView):
    template_name = 'dashboard/customer/address/address-list.html'


    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)

class CustomerAddressCreateView(LoginRequiredMixin, CustomerAccessPermission, SuccessMessageMixin, CreateView):
    template_name = 'dashboard/customer/address/address-create.html'
    form_class = CustumerAddressCreateFrom
    success_message = _('ایجاد نشانی با موفقیت انجام شد')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('dashboard:customer:address-edit', kwargs={'pk': self.object.pk})

class CustomerAddressEditView(LoginRequiredMixin, CustomerAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/customer/address/address-edit.html'
    form_class = CustumerAddressCreateFrom
    success_message = _('ویرایش نشانی با موفقیت انجام شد')

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)

    def get_success_url(self) -> str:
        return reverse('dashboard:customer:address-edit', kwargs={'pk': self.object.pk})

class CustomerAddressDeleteView(LoginRequiredMixin, CustomerAccessPermission, SuccessMessageMixin, DeleteView):
    template_name = 'dashboard/customer/address/address-delete.html'
    success_url = reverse_lazy('dashboard:customer:address-list')
    success_message = _('حذف نشانی با موفقیت انجام شد')

    def get_queryset(self):
        return UserAddressModel.objects.filter(user=self.request.user)
