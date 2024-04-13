from django import forms
from shop.models import ProductModel


class AdminProductEditForm(forms.ModelForm):

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
