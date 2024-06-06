from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ticket.models import TicketModel, TicketStatus
from ..filters import AdminTicketFilter
from ..forms import TicketModelForm
from ...permissions import AdminAccessPermission


class AdminTicketListView(LoginRequiredMixin, AdminAccessPermission, ListView):
    template_name = 'dashboard/admin/ticket/ticket-list.html'
    queryset = TicketModel.objects.all()
    extra_context = {'status_types': TicketStatus.choices}
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        qs = super().get_queryset()
        return AdminTicketFilter(self.request.GET, qs).qs


class AdminTicketEditView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/ticket/ticket-edit.html'
    queryset = TicketModel.objects.all()
    form_class = TicketModelForm
    extra_context = {'status_types': TicketStatus.choices}
    success_message = _('تیکت با موفقیت ویرایش شد')

    def get_success_url(self):
        return reverse('dashboard:admin:ticket-edit', kwargs={'pk': self.object.pk})
