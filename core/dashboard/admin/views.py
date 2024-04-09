from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from ..permissions import AdminAccessPermission
from .forms import AdminPasswordChangeForm, AdminProfileEditForm

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
