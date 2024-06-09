from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from payment.models import PaymentClient
from .models import UserAddressModel, CuponModel


class CheckOutForm(forms.Form):
    address = forms.IntegerField(required=True)
    cupon = forms.CharField(required=False)
    payment = forms.IntegerField(required=True)

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

    def clean_cupon(self):
        code = self.cleaned_data.get('cupon')
        if not code:
            return None

        user = self.request.user

        try:
            cupon_obj = CuponModel.objects.get(code=code)
        except CuponModel.DoesNotExist:
            raise forms.ValidationError(_('کد تخفیف اشتباه است'))

        if cupon_obj.used_by.all().count() >= cupon_obj.max_limit_usage:
            raise forms.ValidationError(_('تعداد کد تخفیف تمام شده است'))

        elif cupon_obj.expiration_date and cupon_obj.expiration_date < timezone.now():
            raise forms.ValidationError(_('کد تخفیف منقصی شده است'))

        elif user in cupon_obj.used_by.all():
            raise forms.ValidationError(
                _('این کد تخفیف قبلا توسط شما استفاده شده است'))

        return cupon_obj

    def clean_payment(self):
        payment = self.cleaned_data.get('payment')
        if payment not in [choice.value for choice in PaymentClient]:
            raise forms.ValidationError(_('درگاه پرداخت نامعتبر است'))
        return payment
