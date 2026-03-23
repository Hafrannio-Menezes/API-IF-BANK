from django.contrib import admin

from apps.goals.models import FinancialGoal


@admin.register(FinancialGoal)
class FinancialGoalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "target_amount", "current_amount", "status", "deadline")
    search_fields = ("title", "user__email", "user__full_name")
    list_filter = ("status", "deadline", "created_at")
    readonly_fields = ("created_at", "updated_at")
