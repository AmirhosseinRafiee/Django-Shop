from django import forms
from django.utils.translation import gettext_lazy as _
from shop.models import FeaturedProductModel


class AdminFeaturedProductForm(forms.ModelForm):
    class Meta:
        model = FeaturedProductModel
        fields = ['product']
        error_messages = {
            'product': {
                'unique': _("این محصول قبلاً به عنوان محصول ویژه انتخاب شده است."),
                'required': _("لطفاً محصولی را انتخاب کنید."),
                'invalid': _("محصول نامعتبر است."),
                'invalid_choice': _("یک محصول معتبر انتخاب کنید. این محصول یکی از انتخاب های موجود نیست."),
            },
        }
