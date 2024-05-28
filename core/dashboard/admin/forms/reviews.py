from django import forms
from django.utils.translation import gettext_lazy as _
from review.models import ReviewProductModel


class ReviewForm(forms.ModelForm):

    class Meta:
        model = ReviewProductModel
        fields = ('status', 'description')
        labels = {
            'status': _('وضعیت'),
            'description': _('توضیحات'),
        }
        help_texts = {
            'status': _('وضعیت نظر را انتخاب کنید'),
            'description': _('توضیحات خود را در مورد محصول وارد کنید'),
        }
        error_messages = {
            'status': {
                'required': _('انتخاب وضعیت الزامی است'),
                'invalid_choice': _('یک وضعیت معتبر را انتخاب کنید این وضعیت یکی از انتخاب‌های موجود نیست'),
            },
            'description': {
                'required': _('نوشتن توضیحات الزامی است'),
                'max_length': _('توضیحات نمی‌تواند بیش از %(limit_value)s حرف باشد'),
            },
        }
