from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [
    path('contact/', views.CreateTicketView.as_view(), name='contact'),
]
