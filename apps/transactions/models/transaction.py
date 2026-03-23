from django.db import models
from django.db.models import Q

from apps.accounts.models import BankAccount


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAWAL = "WITHDRAWAL", "Withdrawal"
        TRANSFER_OUT = "TRANSFER_OUT", "Transfer Out"
        TRANSFER_IN = "TRANSFER_IN", "Transfer In"

    class TransactionStatus(models.TextChoices):
        COMPLETED = "COMPLETED", "Completed"
        FAILED = "FAILED", "Failed"

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="transactions")
    destination_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        related_name="incoming_transfer_references",
        null=True,
        blank=True,
    )
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=TransactionStatus.choices)
    reference_code = models.CharField(max_length=25, unique=True)
    balance_after = models.DecimalField(max_digits=14, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(check=Q(amount__gt=0), name="transactions_amount_positive"),
            models.CheckConstraint(check=Q(balance_after__gte=0), name="transactions_balance_after_non_negative"),
        ]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self) -> str:
        return f"{self.reference_code} - {self.transaction_type}"
