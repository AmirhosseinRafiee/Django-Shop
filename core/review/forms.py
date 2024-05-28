from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ReviewProductModel


class ReviewProductForm(forms.ModelForm):
    class Meta:
        model = ReviewProductModel
        fields = ['product', 'rate', 'description']
        labels = {
            'product': _('محصول'),
            'rate': _('امتیاز'),
            'description': _('توضیحات'),
        }
        help_texts = {
            'rate': _('به محصول از 1 تا 5 امتیاز دهید'),
        }
        error_messages = {
            'product': {
                'required': _('انتخاب محصول الزامی است'),
                'invalid_choice': _('یک محصول معتبر را انتخاب کنید. این محصول یکی از انتخاب‌های موجود نیست'),
            },
            'rate': {
                'required': _('امتیاز دادن الزامی است'),
                'min_value': _('امتیاز نمی‌تواند کمتر از 1 باشد'),
                'max_value': _('امتیاز نمی‌تواند بیشتر از 5 باشد'),
            },
            'description': {
                'required': _('نوشتن توضیحات الزامی است'),
            },
        }
