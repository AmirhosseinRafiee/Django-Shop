from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from shop.models import ProductModel, ProductImageModel


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class AdminProductForm(forms.ModelForm):
    extra_images = MultipleImageField(max_length=1024*1024)

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

    def save(self, commit=True):
        extra_images = self.cleaned_data.pop('extra_images')
        product =  super().save(commit)
        for image in extra_images:
           ProductImageModel(file=image, product=product).save()
        return product