from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django import forms
from accounts.models import Profile

class AdminPasswordChangeForm(PasswordChangeForm):
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

class AdminProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']
