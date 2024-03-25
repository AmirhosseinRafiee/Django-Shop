from django.contrib.auth import views as auth_views
from .forms import CustomAuthentiactionForm

class CustomLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = CustomAuthentiactionForm
    redirect_authenticated_user = True

class CustomLogoutView(auth_views.LogoutView):
    http_method_names = ["post", "options"]
