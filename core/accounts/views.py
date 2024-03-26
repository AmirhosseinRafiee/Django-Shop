from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import CustomAuthentiactionForm, CustomPasswordResetForm

class CustomLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = CustomAuthentiactionForm
    redirect_authenticated_user = True

class CustomLogoutView(auth_views.LogoutView):
    http_method_names = ["post", "options"]


class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password-reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/password-reset-email.html'
    subject_template_name = 'accounts/password-reset-subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('website:index')

class CustomPasswordResetConfirmView(SuccessMessageMixin, auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password-reset-confirm.html'
    success_message = "Password changed successfully."
    success_url = reverse_lazy('accounts:login')
