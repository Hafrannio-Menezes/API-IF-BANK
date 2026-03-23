from django.db import models
from django.db.models import Q

from apps.accounts.models import BankAccount
from common.utils.models import TimeStampedModel


class PortfolioPosition(TimeStampedModel):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="portfolio_positions")
    product = models.ForeignKey("investments.InvestmentProduct", on_delete=models.CASCADE, related_name="positions")
    invested_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    current_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(check=Q(invested_amount__gte=0), name="portfolio_invested_amount_non_negative"),
            models.CheckConstraint(check=Q(current_balance__gte=0), name="portfolio_current_balance_non_negative"),
        ]
        verbose_name = "Portfolio position"
        verbose_name_plural = "Portfolio positions"

    def __str__(self) -> str:
        return f"{self.account.account_number} - {self.product.name}"
