from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [
    path('contact/', views.CreateTicketView.as_view(), name='contact'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
]
