from django import forms
from .models import UserAddressModel


class CheckOutForm(forms.Form):
    address = forms.IntegerField(required=True, )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_address(self):
        try:
            address_obj = UserAddressModel.objects.get(
                user=self.request.user,
                id=self.cleaned_data.get('address')
            )
        except UserAddressModel.DoesNotExist:
            raise forms.ValidationError("Invalid address ID.")

        return address_obj
