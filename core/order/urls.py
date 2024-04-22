from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.OrderCheckoutView.as_view(), name='checkout'),
    path('completed/', views.OrderCompletedView.as_view(), name='completed'),
    path('validate-cupon/', views.OrderValidateCuponView.as_view(), name='validate-cupon'),
]