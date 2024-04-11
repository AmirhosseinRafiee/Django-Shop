from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile

class CustomerPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        "password_incorrect": _(
            "پسورد قبلی شما اشتباه وارد شده است، لطفا تصحیح نمایید."
        ),
        "password_mismatch": _("دو پسورد ورودی با همدیگر مطابقت ندارند"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = "پسورد قبلی خود را وارد نمایید"
        self.fields['new_password1'].widget.attrs['placeholder'] = "پسورد جایگزین خود را وارد نمایید"
        self.fields['new_password2'].widget.attrs['placeholder'] = "پسورد جایگزین خود را مجدد وارد نمایید"

class CustomerProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']

class CustomerProfileImageEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image == self.instance.image:
            raise forms.ValidationError(_("لطفاً یک تصویر را انتخاب کنید"))

        filesize = image.size
        if filesize > 2 * 1024 * 1024:
            raise forms.ValidationError(_("حداکثر اندازه فایل قابل بارگذاری ۲ مگابایت است"))

        return image
