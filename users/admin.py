from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, DoctorUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "role",)
    list_filter = ("email", "is_staff", "is_active", "role",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": (
            "is_staff", "is_active", "role", "groups", "user_permissions",
        )}
        ),
    )
    add_fieldsets = (
        (
            None, {
                "classes": ("wide",),
                "fields": (
                    "email", "password1", "password2", "is_staff",
                    "is_active", "role", "groups", "user_permissions"
                )
            }
        ),
    )
    search_fields = ("email", "role",)
    ordering = ("email", "role",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DoctorUser)
