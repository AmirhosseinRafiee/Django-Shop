from django.urls import path, include

app_name = 'admin'

urlpatterns = [
    path('', include('dashboard.admin.urls.generals')),
    path('', include('dashboard.admin.urls.profiles')),
    path('product/', include('dashboard.admin.urls.products')),
    path('featured-product/', include('dashboard.admin.urls.featured_products')),
    path('coupon/', include('dashboard.admin.urls.coupon')),
    path('user/', include('dashboard.admin.urls.users')),
    path('order/', include('dashboard.admin.urls.orders')),
    path('review/', include('dashboard.admin.urls.reviews')),
    path('ticket/', include('dashboard.admin.urls.tickets')),
    path('newsletter/', include('dashboard.admin.urls.newsletters')),
]