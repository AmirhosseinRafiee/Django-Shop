from django.urls import path, include

app_name = 'customer'

urlpatterns = [
    path('', include('dashboard.customer.urls.generals')),
    path('', include('dashboard.customer.urls.profiles')),
    path('address/', include('dashboard.customer.urls.addresses')),
    path('order/', include('dashboard.customer.urls.orders')),
]