from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.CustomerOrderListView.as_view(), name='order-list'),
    path('<int:pk>/detail/', views.CustomerOrderEditView.as_view(), name='order-detail'),
    path('<int:pk>/invoice/', views.CustomerOrderInvoiceView.as_view(), name='order-invoice'),
]
