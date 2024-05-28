from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('submit/', views.ReviewProductSubmitView.as_view(), name='review-submit'),
]