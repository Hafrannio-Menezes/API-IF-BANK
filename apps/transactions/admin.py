from django.contrib import admin

from apps.transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "transaction_type",
        "amount",
        "status",
        "reference_code",
        "created_at",
    )
    search_fields = ("reference_code", "description", "account__account_number", "account__user__email")
    list_filter = ("transaction_type", "status", "created_at")
    readonly_fields = ("created_at",)
