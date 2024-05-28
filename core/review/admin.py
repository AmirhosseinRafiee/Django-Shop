from django.contrib import admin
from .models import ReviewProductModel


@admin.register(ReviewProductModel)
class ReviewPeoductModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "rate",
        "status",
        "created_date"
    )
    list_filter = ('status',)
