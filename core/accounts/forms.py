from django import forms
from django.contrib.auth import password_validation, forms as auth_forms, get_user_model
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .utils import EmailThread, send_verification_email

User = get_user_model()

class CustomAuthentiactionForm(auth_forms.AuthenticationForm):
    error_messages = {
        'invalid_login': _('لطفاً نام کاربری و گذرواژه صحیح وارد کنید'),
        'inactive': _('این حساب کاربری غیر فعال است'),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages['required'] = _('وارد کردن نام کاربری الزامی است')
        self.fields['password'].error_messages['required'] = _('وارد کردن گذرواژه الزامی است')

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if not user.is_verified:
            send_verification_email(self.request, user)
            raise ValidationError(_('حساب کاربری تایید نشده است. ایمیلی برای تایید حساب به شما ارسال شد'))

class CustomPasswordResetForm(PasswordResetForm):

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        EmailThread(email_message).start()

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("رمزهای عبور همخوانی ندارند."),
        'password_too_similar': _("این رمز عبور خیلی مشابه سایر اطلاعات است."),
        'password_too_short': _("رمز عبور باید حداقل 8 کاراکتر باشد."),
        'password_too_common': _("این رمز عبور خیلی رایج است."),
        'password_entirely_numeric': _("رمز عبور نباید تماماً عددی باشد."),
    }

    class Meta:
        model = User
        fields = ('email',)
        labels = {
            'email': _("آدرس ایمیل"),
            'password1': _("رمز عبور"),
            'password2': _("تکرار رمز عبور"),
        }
        error_messages = {
            'email': {
                'unique': _("این ایمیل قبلاً ثبت شده است."),
                'required': _("وارد کردن ایمیل الزامی است."),
                'invalid': _("ایمیل وارد شده معتبر نمی‌باشد."),
            },
            'password1': {
                'required': _("وارد کردن رمزعبور الزامی است."),
            },
            'password2': {
                'required': _("وارد کردن تکرار رمزعبور الزامی است."),
            }
        }

    def _post_clean(self):
        super(forms.ModelForm, self)._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password1")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password1", self.error_messages.get(error.error_list[0].code, _('رمزعبور بهتری انتخاب کنید')))

