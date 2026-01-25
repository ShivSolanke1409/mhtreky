from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OrganizerProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        "email",
        "phone",
        "is_customer",
        "is_organizer",
        "is_staff",
        "is_active",
    )

    list_filter = ("is_staff", "is_organizer", "is_customer", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        (
            "Roles",
            {"fields": ("is_customer", "is_organizer", "is_staff", "is_active")},
        ),
        (
            "Permissions",
            {"fields": ("groups", "user_permissions")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone", "password1", "password2"),
            },
        ),
    )

    search_fields = ("email", "phone")
    ordering = ("email",)


@admin.register(OrganizerProfile)
class OrganizerProfileAdmin(admin.ModelAdmin):
    list_display = ("organization_name", "contact_person", "phone", "created_at")
    search_fields = ("organization_name", "contact_person")
