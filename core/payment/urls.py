from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('order/<int:pk>/pay/zp/', views.ZarinpalPayView.as_view(), name='zarinpal-pay'),
    path('verify/zp/', views.ZarinpalVerifyView.as_view(), name='zarinpal-verify'),
]