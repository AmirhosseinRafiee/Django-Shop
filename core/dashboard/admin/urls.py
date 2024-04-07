from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    path('home/', views.AdminDashboradHomeView.as_view(), name='home'),
]