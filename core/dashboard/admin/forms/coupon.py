
from django import forms
from order.models import CuponModel
from django.utils.translation import gettext_lazy as _

class AdminCouponForm(forms.ModelForm):

    class Meta:
        model = CuponModel
        fields = [
            'code',
            'discount_percent',
            'max_discount_amount',
            'max_limit_usage',
            'expiration_date',
        ]
        error_messages = {
            'code': {
                'unique': _("تخفیفی با این کد قبلا ساخته شده است"),
            },
            'discount_percent': {
                'min_value': _("مقدار نمی‌تواند کمتر از %(limit_value)s باشد"),
                'max_value': _("مقدار نمی‌تواند بیشتر از %(limit_value)s باشد"),
            },
            'max_discount_amount': {
                'invalid': _("مقدار وارد شده معتبر نمی‌باشد"),
            },
            'max_limit_usage': {
                'invalid': _("مقدار وارد شده معتبر نمی‌باشد"),
            },
            'expiration_date': {
                'invalid': _("تاریخ انقضا باید به فرمت صحیح باشد"),
            },
        }
