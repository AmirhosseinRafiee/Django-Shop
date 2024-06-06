from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.AdminNewsletterListView.as_view(), name='newsletter-list'),
]