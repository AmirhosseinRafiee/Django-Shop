from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.AdminOrderListView.as_view(), name='order-list'),
    path('<int:pk>/edit/', views.AdminOrderEditView.as_view(), name='order-edit'),
]