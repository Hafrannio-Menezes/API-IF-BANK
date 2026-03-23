from django.conf import settings
from django.db import models
from django.db.models import Q

from common.utils.models import TimeStampedModel


class FinancialGoal(TimeStampedModel):
    class GoalStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        ACHIEVED = "ACHIEVED", "Achieved"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="financial_goals")
    title = models.CharField(max_length=150)
    target_amount = models.DecimalField(max_digits=14, decimal_places=2)
    current_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    deadline = models.DateField()
    status = models.CharField(max_length=15, choices=GoalStatus.choices, default=GoalStatus.ACTIVE)

    class Meta:
        ordering = ["deadline", "-created_at"]
        constraints = [
            models.CheckConstraint(check=Q(target_amount__gt=0), name="goals_target_amount_positive"),
            models.CheckConstraint(check=Q(current_amount__gte=0), name="goals_current_amount_non_negative"),
        ]
        verbose_name = "Financial goal"
        verbose_name_plural = "Financial goals"

    def __str__(self) -> str:
        return self.title
