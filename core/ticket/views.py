from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import TicketForm

class CreateTicketView(SuccessMessageMixin, CreateView):
    form_class = TicketForm
    template_name = 'website/contact.html'
    success_url = reverse_lazy('ticket:contact')
    success_message = 'تیکت شما با موفقیت ارسال شد'
