from django.urls import path
from .. import views

urlpatterns = [
    path('home/', views.CustomerDashboradHomeView.as_view(), name='home'),
]