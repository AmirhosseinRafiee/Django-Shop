from django import forms
from django.utils.translation import gettext_lazy as _
from .models import TicketModel, NewsletterSubscriberModel

class TicketForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'description']
        error_messages = {
            'first_name': {
                'required': "وارد کردن نام الزامی است.",
                'max_length': "نام نمی‌تواند بیش از ۵۰ کاراکتر باشد.",
            },
            'last_name': {
                'required': "وارد کردن نام خانوادگی الزامی است.",
                'max_length': "نام خانوادگی نمی‌تواند بیش از ۵۰ کاراکتر باشد.",
            },
            'email': {
                'required': "وارد کردن ایمیل الزامی است.",
                'invalid': "لطفاً یک ایمیل معتبر وارد کنید.",
            },
            'phone_number': {
                'invalid': "لطفاً یک شماره تلفن معتبر وارد کنید.",
                'max_length': "شماره تلفن نمی‌تواند بیش از ۱۵ کاراکتر باشد.",
            },
            'description': {
                'required': "وارد کردن توضیحات الزامی است.",
            },
        }



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
