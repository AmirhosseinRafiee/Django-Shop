from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import ReviewProductModel
from .forms import ReviewProductForm

class ReviewProductSubmitView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    http_method_names = ['post']
    form_class = ReviewProductForm

    def form_valid(self, form: ReviewProductForm):
        product = form.instance.product

        # Check if the product is published
        if product.status != 'published':
            messages.error(self.request, _('یک محصول معتبر را انتخاب کنید. این محصول یکی از انتخاب‌های موجود نیست'))
            return redirect(self.request.META.get('HTTP_REFERER'))

        self.deleted_count = self._delete_existing_reviews(form.instance.product)
        form.instance.user = self.request.user
        form.instance.is_buyer = form.instance.is_user_buyer()
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return redirect(self.request.META.get('HTTP_REFERER'))

    def get_success_url(self):
        return reverse('shop:product-detail', kwargs={'slug': self.object.product.slug})

    def get_success_message(self, cleaned_data):
        if self.deleted_count > 0:
            return _('دیدگاه با موفقیت جایگزین دیدگاه قبلی شد و پس از تایید منتشر میشود')
        return _('دیدگاه با موفقیت ثبت شد و پس از تایید منتشر میشود')

    def _delete_existing_reviews(self, product) -> int:
        return ReviewProductModel.objects.filter(user=self.request.user, product=product).delete()[0]
