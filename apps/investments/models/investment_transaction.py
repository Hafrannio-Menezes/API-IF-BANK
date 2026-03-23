from django.db import models
from django.db.models import Q


class InvestmentTransaction(models.Model):
    class TransactionType(models.TextChoices):
        APPLY = "APPLY", "Apply"
        REDEEM = "REDEEM", "Redeem"

    position = models.ForeignKey(
        "investments.PortfolioPosition",
        on_delete=models.CASCADE,
        related_name="investment_transactions",
    )
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    reference_code = models.CharField(max_length=25, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(check=Q(amount__gt=0), name="investment_transaction_amount_positive"),
        ]
        verbose_name = "Investment transaction"
        verbose_name_plural = "Investment transactions"

    def __str__(self) -> str:
        return f"{self.reference_code} - {self.transaction_type}"
