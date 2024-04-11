from django.urls import path
from .. import views

urlpatterns = [
    path('home/', views.AdminDashboradHomeView.as_view(), name='home'),
]