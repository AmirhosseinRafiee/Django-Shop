from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.AdminFeaturedProductListView.as_view(), name='featured-product-list'),
    path('create/', views.AdminFeaturedProductCreateView.as_view(), name='featured-product-create'),
    path('delete/<int:pk>/', views.AdminFeaturedProductDeleteView.as_view(), name='featured-product-delete'),
]