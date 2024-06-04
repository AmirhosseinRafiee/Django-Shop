from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.forms import BaseForm
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from .forms import CustomAuthentiactionForm, CustomPasswordResetForm, CustomUserCreationForm
from .tokens import account_activation_token
from .utils import send_verification_email

User = get_user_model()


class AnonymousRequiredMixin:
    redirect_url = reverse_lazy('website:index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = CustomAuthentiactionForm
    redirect_authenticated_user = True


class CustomLogoutView(LoginRequiredMixin, auth_views.LogoutView):
    http_method_names = ["post", "options"]


class CustomPasswordResetView(AnonymousRequiredMixin, SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password-reset.html'
    form_class = CustomPasswordResetForm
    subject_template_name = 'accounts/email/password-reset-subject.txt'
    email_template_name = 'accounts/email/password-reset-email.html'
    html_email_template_name = 'accounts/email/password-reset-email-html.html'
    success_message = _(
        'اگر حسابی با ایمیل وارد شده وجود داشته باشد. به زودی ایمیلی برای تغییر رمزعبور دریافت خواهید کرد')
    success_url = reverse_lazy('website:index')


class CustomPasswordResetConfirmView(AnonymousRequiredMixin, SuccessMessageMixin, auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password-reset-confirm.html'
    success_message = _('رمزعبور با موفقیت تغییر کرد')
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                messages.warning(
                    _('تشخیص حلقه تغییر مسیر برای کاربر احراز هویت شده'))
                return redirect('website:index')
            return redirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


class CustomSignUpView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm
    success_message = _(
        'ایمیلی برای تایید حساب کاربری به شما ارسال شد. پس از تایید آن میتوانید وارد شوید')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                messages.warning(
                    _('تشخیص حلقه تغییر مسیر برای کاربر احراز هویت شده'))
                return redirect('website:index')
            return redirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('accounts:login')

    def form_valid(self, form: BaseForm) -> HttpResponse:
        response = super().form_valid(form)
        send_verification_email(self.request, self.object)
        return response


class EmailVerifyView(AnonymousRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(kwargs.get('uidb64')))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, kwargs.get('token')):
            user.is_verified = True
            user.save()
            messages.success(request, _(
                'حساب شما فعال شد اکنون میتوانید وارد شوید'))
        else:
            messages.warning(request, _(
                'لینک معتبر نیست. وارد شوید تا مجددا ایمیل تایید برای شما ارسال شود'))
        return redirect('accounts:login')
