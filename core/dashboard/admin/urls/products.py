from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.AdminProductListView.as_view(), name='product-list'),
    path('create/', views.AdminProductCreateView.as_view(), name='product-create'),
    path('edit/<int:pk>/', views.AdminProductEditView.as_view(), name='product-edit'),
    path('delete/<int:pk>/', views.AdminProductDeleteView.as_view(), name='product-delete'),
]