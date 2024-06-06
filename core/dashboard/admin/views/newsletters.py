from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ticket.models import NewsletterSubscriberModel
from ...permissions import AdminAccessPermission


class AdminNewsletterListView(LoginRequiredMixin, AdminAccessPermission, ListView):
    template_name = 'dashboard/admin/newsletter/newsletter-list.html'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        qs = NewsletterSubscriberModel.objects.all()
        if email := self.request.GET.get('email'):
            qs = qs.filter(email__icontains=email)
        return qs
