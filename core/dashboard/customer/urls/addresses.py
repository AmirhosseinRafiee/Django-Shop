from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.CustomerAddressListView.as_view(), name='address-list'),
    path('create/', views.CustomerAddressCreateView.as_view(), name='address-create'),
    path('<int:pk>/edit/', views.CustomerAddressEditView.as_view(), name='address-edit'),
    path('<int:pk>/delete/', views.CustomerAddressDeleteView.as_view(), name='address-delete'),
]