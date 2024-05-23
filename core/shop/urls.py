from django.urls import path, re_path
from . import views

app_name = 'shop'

urlpatterns = [
    path('product/grid/', views.ShopProductGridView.as_view(), name='product-grid'),
    re_path('product/detail/(?P<slug>[-\w]+)/', views.ShopProductDetailView.as_view(), name='product-detail'),
    path('toggle/', views.WishlistToggleView.as_view(), name='wishlist-toggle'),
]