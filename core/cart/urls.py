from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('session/cart/summary/', views.CartSummaryView.as_view(), name='session-cart-summary'),
    path('session/product-add/', views.SessionAddProductView.as_view(), name='session-add-product'),
    path('session/product-remove/', views.SessionRemoveProductView.as_view(), name='session-remove-product'),
    # path('session/product-clear/', views.SessionClearProductView.as_view(), name='session-clear-product'),
]
