from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.AdminCouponListView.as_view(), name='coupon-list'),
    path('create/', views.AdminCouponCreateView.as_view(), name='coupon-create'),
    path('<int:pk>/edit/', views.AdminCouponEditView.as_view(), name='coupon-edit'),
    path('<int:pk>/delete/', views.AdminCouponDeleteView.as_view(), name='coupon-delete'),
]