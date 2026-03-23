from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "full_name", "cpf", "is_active", "is_staff", "created_at")
    search_fields = ("email", "full_name", "cpf")
    list_filter = ("is_active", "is_staff", "is_superuser")
    readonly_fields = ("created_at", "updated_at", "date_joined", "last_login")

    fieldsets = (
        ("credenciais", {"fields": ("email", "password")}),
        ("dados pessoais", {"fields": ("full_name", "cpf", "phone", "birth_date")}),
        (
            "permissoes",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("auditoria", {"fields": ("date_joined", "last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            "criar usuario",
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )
