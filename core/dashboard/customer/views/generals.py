from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...permissions import CustomerAccessPermission

class CustomerDashboradHomeView(LoginRequiredMixin, CustomerAccessPermission, TemplateView):
    template_name = 'dashboard/customer/home.html'
