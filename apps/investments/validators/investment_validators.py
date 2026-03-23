from decimal import Decimal

from rest_framework.exceptions import ValidationError


def validate_positive_money(amount: Decimal) -> Decimal:
    if amount <= Decimal("0"):
        raise ValidationError({"amount": "Amount must be greater than zero."})
    return amount


def validate_minimum_amount(*, amount: Decimal, minimum_amount: Decimal) -> None:
    if amount < minimum_amount:
        raise ValidationError({"amount": f"Minimum amount for this product is {minimum_amount}."})


def validate_redeem_balance(*, amount: Decimal, available_balance: Decimal) -> None:
    if amount > available_balance:
        raise ValidationError({"amount": "Redeem amount exceeds the invested balance."})
