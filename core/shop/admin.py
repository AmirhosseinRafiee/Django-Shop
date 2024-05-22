from django.contrib import admin
from .models import ProductModel, ProductCategoryModel, ProductImageModel, WishlistProductModel

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "stock", "price", "discount_percent", "status", "created_date")
    list_filter = ("status",)
    search_fields = ("title",)

@admin.register(ProductCategoryModel)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_date")
    search_fields = ("title",)

@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_date")

@admin.register(WishlistProductModel)
class WishlistProductAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")
