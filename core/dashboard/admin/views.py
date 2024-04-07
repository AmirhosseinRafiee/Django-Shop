from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..permissions import AdminAccessPermission

class AdminDashboradHomeView(LoginRequiredMixin, AdminAccessPermission, TemplateView):
    template_name = 'dashboard/admin/home.html'
