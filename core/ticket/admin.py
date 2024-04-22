from django.contrib import admin
from .models import TicketModel, NewsletterSubscriberModel

@admin.register(TicketModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "phone_number", "email", "status")
    search_fields = ("email", "phone_number", "last_name")
    list_filter = ("status",)

@admin.register(NewsletterSubscriberModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
