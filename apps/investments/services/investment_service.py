from datetime import timedelta
from decimal import Decimal

from django.db import transaction as db_transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.accounts.models import BankAccount
from apps.investments.models import InvestmentProduct, InvestmentTransaction, PortfolioPosition
from apps.notifications.models import Notification
from apps.notifications.services import create_notification
from apps.transactions.validators import validate_sufficient_balance
from apps.investments.validators import validate_minimum_amount, validate_positive_money, validate_redeem_balance
from common.utils.identifiers import generate_reference_code


def _get_locked_account_for_user(*, user, account_id: int) -> BankAccount:
    try:
        return BankAccount.objects.select_for_update().get(id=account_id, user=user, is_active=True)
    except BankAccount.DoesNotExist as exc:
        raise ValidationError({"account_id": "Account not found or inactive."}) from exc


def _get_locked_position_for_user(*, user, position_id: int) -> PortfolioPosition:
    try:
        return (
            PortfolioPosition.objects.select_for_update()
            .select_related("product", "account")
            .get(id=position_id, account__user=user)
        )
    except PortfolioPosition.DoesNotExist as exc:
        raise ValidationError({"position_id": "Investment position not found."}) from exc


def apply_investment(*, user, account_id: int, product_id: int, amount: Decimal) -> PortfolioPosition:
    validate_positive_money(amount)

    with db_transaction.atomic():
        account = _get_locked_account_for_user(user=user, account_id=account_id)
        try:
            product = InvestmentProduct.objects.get(id=product_id, is_active=True)
        except InvestmentProduct.DoesNotExist as exc:
            raise ValidationError({"product_id": "Investment product not found or inactive."}) from exc
        validate_minimum_amount(amount=amount, minimum_amount=product.minimum_initial_amount)
        validate_sufficient_balance(balance=account.balance, amount=amount)

        account.balance -= amount
        account.save()
        position = PortfolioPosition.objects.create(
            account=account,
            product=product,
            invested_amount=amount,
            current_balance=amount,
        )

        InvestmentTransaction.objects.create(
            position=position,
            transaction_type=InvestmentTransaction.TransactionType.APPLY,
            amount=amount,
            reference_code=generate_reference_code("INV"),
        )
        create_notification(
            user=user,
            title="Aplicacao realizada",
            message=f"Aplicacao de R$ {amount} no produto {product.name}.",
            notification_type=Notification.NotificationType.INVESTMENT,
        )
        return position


def redeem_investment(*, user, position_id: int, amount: Decimal) -> PortfolioPosition:
    validate_positive_money(amount)

    with db_transaction.atomic():
        position = _get_locked_position_for_user(user=user, position_id=position_id)
        product = position.product
        account = BankAccount.objects.select_for_update().get(id=position.account_id)

        minimum_release_date = position.created_at + timedelta(days=product.term_days)
        if timezone.now() < minimum_release_date:
            raise ValidationError(
                {"position_id": f"This investment can only be redeemed after {minimum_release_date.date()}."}
            )

        validate_redeem_balance(amount=amount, available_balance=position.current_balance)

        position.current_balance -= amount
        position.invested_amount = max(Decimal("0"), position.invested_amount - amount)
        account.balance += amount
        position.save()
        account.save()

        InvestmentTransaction.objects.create(
            position=position,
            transaction_type=InvestmentTransaction.TransactionType.REDEEM,
            amount=amount,
            reference_code=generate_reference_code("RED"),
        )
        create_notification(
            user=user,
            title="Resgate realizado",
            message=f"Resgate de R$ {amount} do produto {product.name}.",
            notification_type=Notification.NotificationType.INVESTMENT,
        )
        return position


def simulate_investment(*, initial_amount: Decimal, annual_rate: Decimal, period_months: int, monthly_contribution: Decimal = Decimal("0")) -> dict:
    validate_positive_money(initial_amount)
    if period_months <= 0:
        raise ValidationError({"period_months": "Investment period must be greater than zero."})
    if annual_rate < Decimal("0"):
        raise ValidationError({"annual_rate": "Annual rate cannot be negative."})
    if monthly_contribution < Decimal("0"):
        raise ValidationError({"monthly_contribution": "Monthly contribution cannot be negative."})

    monthly_rate = (annual_rate / Decimal("100")) / Decimal("12")
    balance = initial_amount
    invested_capital = initial_amount

    for _ in range(period_months):
        balance = (balance * (Decimal("1") + monthly_rate)) + monthly_contribution
        invested_capital += monthly_contribution

    estimated_return = balance - invested_capital
    return {
        "initial_amount": initial_amount,
        "annual_rate": annual_rate,
        "period_months": period_months,
        "monthly_contribution": monthly_contribution,
        "invested_capital": invested_capital.quantize(Decimal("0.01")),
        "estimated_return": estimated_return.quantize(Decimal("0.01")),
        "final_amount": balance.quantize(Decimal("0.01")),
    }
