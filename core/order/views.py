from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import HasCustomerAccessPermission

class OrderCheckoutView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    template_name = 'order/order-checkout.html'
