from django import forms
from django.utils.translation import gettext_lazy as _
from .models import TicketModel, NewsletterSubscriberModel

class TicketForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'description']

class NewsletterSubscriberForm(forms.ModelForm):

    class Meta:
        model = NewsletterSubscriberModel
        fields = ['email']
        error_messages = {
            'email': {
                'required': _('لطفاً ایمیل خود را پر کنید'),
                'unique': _("این آدرس ایمیل قبلا در خبرنامه ما ثبت شده است"),
                'invalid': _("لطفاً یک آدرس ایمیل معتبر وارد کنید"),
            },
        }
