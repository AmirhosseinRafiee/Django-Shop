from django.urls import path
from .. import views

urlpatterns = [
    path('list/', views.AdminReviewListView.as_view(), name='review-list'),
    path('edit/<int:pk>/', views.AdminReviewEditView.as_view(), name='review-edit'),
]