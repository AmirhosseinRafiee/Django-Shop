from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from shop.models import ProductModel


class AdminProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = False

    class Meta:
        model = ProductModel
        fields = [
            'title',
            'slug',
            'stock',
            'status',
            'category',
            'price',
            'discount_percent',
            'brief_description',
            'description',
            'image',
        ]
        widgets = {
            "description": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5",
                    "placeholder": "توضیحات محصول را وارد کنید",
                },
                config_name="extends"
            )
        }
