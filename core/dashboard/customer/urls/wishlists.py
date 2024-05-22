from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.CustomerWishlistListView.as_view(), name='wishlist-list'),
    path('<int:pk>/delete/', views.CustomerWishlistDeleteView.as_view(), name='wishlist-delete'),
]