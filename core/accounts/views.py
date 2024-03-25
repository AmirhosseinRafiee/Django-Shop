from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .forms import CustomAuthentiactionForm

class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = CustomAuthentiactionForm
    redirect_authenticated_user = True
    next_page = '/'
