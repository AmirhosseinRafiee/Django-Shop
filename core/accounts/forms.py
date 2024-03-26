from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import PasswordResetForm
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .utils import EmailThread

class CustomAuthentiactionForm(auth_forms.AuthenticationForm):

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)

        if not user.is_verified:
            raise ValidationError(_('This account is not verified.'))

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
