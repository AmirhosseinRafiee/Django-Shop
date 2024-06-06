from django.views.generic import View, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .forms import TicketForm, NewsletterSubscriberForm

class CreateTicketView(SuccessMessageMixin, CreateView):
    form_class = TicketForm
    template_name = 'website/contact.html'
    success_url = reverse_lazy('ticket:contact')
    success_message = _('تیکت شما با موفقیت ارسال شد')

class NewsletterSubscribeView(View):

    def post(self, request, *args, **kwargs):
        form = NewsletterSubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(data={'message': _('با موفقیت عضو خبرنامه شدید')})

        error_messages = [error[0] for error in form.errors.values()]
        return JsonResponse(data={'error':error_messages[0]}, status=400)
