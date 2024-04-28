from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from ...permissions import AdminAccessPermission

User = get_user_model()

class AdminDashboradUserListView(LoginRequiredMixin, AdminAccessPermission, ListView):
    template_name = 'dashboard/admin/user/user-list.html'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        qs = User.objects.select_related('profile')
        if email := self.request.GET.get('email'):
            qs = qs.filter(email__icontains=email)
        return qs
