from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from accounts.models import UserType


class HasCustomerAccessPermission(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == UserType.customer.value
        return False


class IsOrderDeliveredMixin:
    """
    Mixin to check if an order is successful.
    """

    def get_object(self):
        # Fetch the object once and cache it
        if not hasattr(self, '_cached_object'):
            self._cached_object = super().get_object()
        return self._cached_object

    def dispatch(self, request, *args, **kwargs):
        # Get the object (from cache if already fetched)
        self.object = self.get_object()

        # Check if the order is successful
        if not self.object.is_delivered:
            return HttpResponseForbidden("This order is not delivered.")

        return super().dispatch(request, *args, **kwargs)
