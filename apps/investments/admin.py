from django.contrib import admin

from apps.investments.models import InvestmentProduct, InvestmentTransaction, PortfolioPosition


@admin.register(InvestmentProduct)
class InvestmentProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product_type", "annual_rate", "term_days", "risk_level", "is_active")
    search_fields = ("name",)
    list_filter = ("product_type", "risk_level", "is_active")


@admin.register(PortfolioPosition)
class PortfolioPositionAdmin(admin.ModelAdmin):
    list_display = ("id", "account", "product", "invested_amount", "current_balance", "created_at")
    search_fields = ("account__account_number", "product__name", "account__user__email")
    list_filter = ("product__product_type",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(InvestmentTransaction)
class InvestmentTransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "position", "transaction_type", "amount", "reference_code", "created_at")
    search_fields = ("reference_code", "position__product__name", "position__account__user__email")
    list_filter = ("transaction_type", "created_at")
    readonly_fields = ("created_at",)
