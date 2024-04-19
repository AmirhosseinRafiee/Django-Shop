from django import forms
from django.utils.translation import gettext_lazy as _
from order.models import UserAddressModel


class CustumerAddressCreateFrom(forms.ModelForm):

    class Meta:
        model = UserAddressModel
        fields = [
            "address",
            "state",
            "city",
            "zip_code",
        ]
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'pattern': '\d{10}', 'title': _("کد پستی باید ده رقمی باشد")}),
        }
