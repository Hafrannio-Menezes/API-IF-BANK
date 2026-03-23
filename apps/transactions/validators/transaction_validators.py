from decimal import Decimal

from rest_framework.exceptions import ValidationError


def validate_positive_amount(amount: Decimal) -> Decimal:
    if amount <= Decimal("0"):
        raise ValidationError({"amount": "Amount must be greater than zero."})
    return amount


def validate_sufficient_balance(*, balance: Decimal, amount: Decimal) -> None:
    if balance < amount:
        raise ValidationError({"amount": "Insufficient balance for this operation."})
