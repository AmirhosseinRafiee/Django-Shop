from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.AdminProductListView.as_view(), name='product-list'),
]