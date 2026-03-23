from decimal import Decimal

from rest_framework.exceptions import ValidationError


def validate_initial_balance(value: Decimal) -> Decimal:
    if value < Decimal("0"):
        raise ValidationError("Initial balance cannot be negative.")
    return value
