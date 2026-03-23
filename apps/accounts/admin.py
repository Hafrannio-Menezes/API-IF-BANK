from django.contrib import admin

from apps.accounts.models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "agency_number",
        "account_number",
        "account_type",
        "balance",
        "is_active",
        "created_at",
    )
    search_fields = ("account_number", "agency_number", "user__email", "user__full_name")
    list_filter = ("account_type", "is_active")
    readonly_fields = ("created_at", "updated_at")
