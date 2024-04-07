from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import UserType

class DashboradHomeView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.type == UserType.customer.value:
                return redirect(reverse('dashboard:customer:home'))
            elif request.user.type == UserType.admin.value:
                return redirect(reverse('dashboard:admin:home'))

        return super().dispatch(request, *args, **kwargs)



