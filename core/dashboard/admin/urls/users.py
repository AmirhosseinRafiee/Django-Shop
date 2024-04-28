from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.AdminDashboradUserListView.as_view(), name='user-list'),
]