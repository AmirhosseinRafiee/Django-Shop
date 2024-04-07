from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('home/', views.CustomerDashboradHomeView.as_view(), name='home'),
]