from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "email", "is_superuser", "is_staff", "is_active", "is_verified")
    list_filter = ("type", "is_superuser", "is_staff", "is_active", "is_verified")
    search_fields = ("email",)
    ordering = ("created_date",)
    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                )
            },
        ),
        ("Group Permissions", {"fields": ("groups", "user_permissions", "type")}),
        ("important date", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type"
                ),
            },
        ),
    )

class ProfileAdmin(admin.ModelAdmin):
    model = User
    list_display = ("id", "user", "first_name", "last_name", "phone_number")
    list_filter = ("gender",)
    search_fields = ("user", "phone_number", "last_name", "first_name")
    ordering = ("created_date",)

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Session, SessionAdmin)
