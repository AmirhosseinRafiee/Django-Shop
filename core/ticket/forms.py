from django import forms
from .models import TicketModel

class TicketForm(forms.ModelForm):
    class Meta:
        model = TicketModel
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'description']
