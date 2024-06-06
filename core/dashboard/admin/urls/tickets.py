from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.AdminTicketListView.as_view(), name='ticket-list'),
    path('<int:pk>/edit/', views.AdminTicketEditView.as_view(), name='ticket-edit'),
]