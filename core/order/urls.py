from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.OrderCheckoutView.as_view(), name='checkout'),
]