from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.CustomSignUpView.as_view(), name='signup'),
    path('verify-email-confirm/<uidb64>/<token>/', views.EmailVerifyView.as_view(), name='verify-email-confirm'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
        views.CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
]

