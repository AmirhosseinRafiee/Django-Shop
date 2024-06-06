from django import forms
from django.utils.translation import gettext_lazy as _
from ticket.models import TicketModel

class TicketModelForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        fields = ['status']
        error_messages = {
            'status': {
                'required': _('وارد کردن وضعیت تیکت الزامی است'),
                'invalid': _('وضعیت تیکت معتبر نیست'),
                'invalid_choice': _('انتخاب معتبر نیست'),
            },
        }