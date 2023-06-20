from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("id", "email", "is_staff", "is_verified", "role")
    list_filter = ("is_staff", "role")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": (
            "is_staff", "is_active", "role"
        )}
        ),
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": (
                    "email", "password1", "password2", "is_staff",
                    "is_active", "role",
                )
            }
        ),
    )
    search_fields = ("email", "role",)
    ordering = ("email", "role",)
