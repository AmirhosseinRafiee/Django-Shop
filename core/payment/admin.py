from django.contrib import admin
from .models import PaymentModel


@admin.register(PaymentModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        'order',
        'client',
        'amount',
        'status',
        'authority_id',
        'created_date',
    )
    list_filter = ('status', 'client')
