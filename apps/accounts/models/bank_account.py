from django.conf import settings
from django.db import models
from django.db.models import Q

from common.utils.models import TimeStampedModel


class BankAccount(TimeStampedModel):
    class AccountType(models.TextChoices):
        CHECKING = "CHECKING", "Checking"
        SAVINGS = "SAVINGS", "Savings"
        INVESTMENT = "INVESTMENT", "Investment"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=20, unique=True)
    agency_number = models.CharField(max_length=10)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(check=Q(balance__gte=0), name="accounts_balance_non_negative"),
        ]
        verbose_name = "Bank account"
        verbose_name_plural = "Bank accounts"

    def __str__(self) -> str:
        return f"{self.account_number} - {self.user.email}"
