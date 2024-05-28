from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from review.models import ReviewProductModel, ReviewStatusType
from ...permissions import AdminAccessPermission
from ..forms import ReviewForm
from ..filters import AdminReviewFilter


class AdminReviewListView(LoginRequiredMixin, AdminAccessPermission, ListView):
    template_name = 'dashboard/admin/review/review-list.html'
    queryset = ReviewProductModel.objects.all().select_related('user__profile', 'product')
    extra_context = {'review_status': ReviewStatusType.choices}
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        qs = super().get_queryset()
        return AdminReviewFilter(self.request.GET, qs).qs

class AdminReviewEditView(LoginRequiredMixin, AdminAccessPermission, SuccessMessageMixin, UpdateView):
    template_name = 'dashboard/admin/review/review-edit.html'
    queryset = ReviewProductModel.objects.all().select_related('user__profile', 'product')
    form_class = ReviewForm
    extra_context = {'review_status': ReviewStatusType.choices}
    success_message = _('تغییرات با موفقیت اعمال شد')

    def get_success_url(self):
        return reverse('dashboard:admin:review-edit', kwargs={'pk': self.object.pk})

