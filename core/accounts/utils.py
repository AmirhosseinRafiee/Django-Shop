import threading
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext_lazy as _
from .tokens import account_activation_token


class EmailThread(threading.Thread):
    # overriding constructor
    def __init__(self, email_obj):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()

def send_email(subject, message, email, html_message=None):
    email = EmailMultiAlternatives(
                subject, message, to=[email]
            )
    if html_message:
        email.attach_alternative(html_message, "text/html")

    EmailThread(email).start()

def send_verification_email(request, user):
    current_site = get_current_site(request)
    email = user.email
    subject = _('تایید ایمیل')
    context = {
        'request': request,
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    message = render_to_string('accounts/email/verify_email_message.html', context)
    html_message = render_to_string('accounts/email/verify_email_message-html.html', context)
    send_email(subject, message, email, html_message)