from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from ...permissions import CustomerAccessPermission
from ..forms import CustomerPasswordChangeForm, CustomerProfileEditForm, CustomerProfileImageEditForm

class CustomerSecurotyEditView(LoginRequiredMixin, CustomerAccessPermission, SuccessMessageMixin, PasswordChangeView):
    template_name = 'dashboard/customer/profile/security-edit.html'
    form_class = CustomerPasswordChangeForm
    success_url = reverse_lazy('dashboard:customer:security-edit')
    success_message = _('بروز رسانی رمزعبور با موفقیت انجام شد')

class CustomerProfileEditView(LoginRequiredMixin, CustomerAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/customer/profile/profile-edit.html'
    form_class = CustomerProfileEditForm
    success_url = reverse_lazy('dashboard:customer:profile-edit')
    success_message = _('بروز رسانی پروفایل با موفقیت انجام شد')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

class CustomerProfileImageEditView(LoginRequiredMixin, CustomerAccessPermission, SuccessMessageMixin, UpdateView):
    http_method_names = ['post']
    form_class = CustomerProfileImageEditForm
    success_url = reverse_lazy('dashboard:customer:profile-edit')
    success_message = _('بروز رسانی  عکس پروفایل با موفقیت انجام شد')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.success_url)