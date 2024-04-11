from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from ..permissions import AdminAccessPermission
from .forms import AdminPasswordChangeForm, AdminProfileEditForm, AdminProfileImageEditForm

class AdminDashboradHomeView(LoginRequiredMixin, AdminAccessPermission, TemplateView):
    template_name = 'dashboard/admin/home.html'

class AdminSecurotyEditView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, PasswordChangeView):
    template_name = 'dashboard/admin/profile/security-edit.html'
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy('dashboard:admin:securiyt-edit')
    success_message = _('بروز رسانی رمزعبور با موفقیت انجام شد')

class AdminProfileEditView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/profile/profile-edit.html'
    form_class = AdminProfileEditForm
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = _('بروز رسانی پروفایل با موفقیت انجام شد')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

class AdminProfileImageEditView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, UpdateView):
    http_method_names = ['post']
    form_class = AdminProfileImageEditForm
    success_url = reverse_lazy('dashboard:admin:profile-edit')
    success_message = _('بروز رسانی  عکس پروفایل با موفقیت انجام شد')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.success_url)