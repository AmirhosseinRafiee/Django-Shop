from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.models import UserType

class CustomerAccessPermission(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.type == UserType.customer.value

class AdminAccessPermission(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.type == UserType.admin.value
