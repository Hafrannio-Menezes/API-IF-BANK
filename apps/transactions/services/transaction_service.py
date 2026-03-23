from decimal import Decimal

from django.db import transaction as db_transaction
from rest_framework.exceptions import ValidationError

from apps.accounts.models import BankAccount
from apps.notifications.models import Notification
from apps.notifications.services import create_notification
from apps.transactions.models import Transaction
from apps.transactions.validators import validate_positive_amount, validate_sufficient_balance
from common.utils.identifiers import generate_reference_code


def _get_locked_account(*, account_id: int, user) -> BankAccount:
    try:
        return BankAccount.objects.select_for_update().get(id=account_id, user=user, is_active=True)
    except BankAccount.DoesNotExist as exc:
        raise ValidationError({"account_id": "Account not found or inactive."}) from exc


def _get_locked_destination_account(*, account_id: int) -> BankAccount:
    try:
        return BankAccount.objects.select_for_update().get(id=account_id, is_active=True)
    except BankAccount.DoesNotExist as exc:
        raise ValidationError({"destination_account_id": "Destination account not found or inactive."}) from exc


def _get_locked_transfer_accounts(*, user, source_account_id: int, destination_account_id: int) -> tuple[BankAccount, BankAccount]:
    locked_accounts = {
        account.id: account
        for account in BankAccount.objects.select_for_update()
        .filter(id__in=sorted([source_account_id, destination_account_id]), is_active=True)
        .order_by("id")
    }

    source_account = locked_accounts.get(source_account_id)
    destination_account = locked_accounts.get(destination_account_id)

    if source_account is None or source_account.user_id != user.id:
        raise ValidationError({"source_account_id": "Source account not found or inactive."})
    if destination_account is None:
        raise ValidationError({"destination_account_id": "Destination account not found or inactive."})

    return source_account, destination_account


def deposit(*, user, account_id: int, amount: Decimal, description: str = "") -> Transaction:
    validate_positive_amount(amount)

    with db_transaction.atomic():
        account = _get_locked_account(account_id=account_id, user=user)
        account.balance += amount
        account.save()

        transaction = Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TransactionType.DEPOSIT,
            amount=amount,
            description=description or "Deposito realizado.",
            status=Transaction.TransactionStatus.COMPLETED,
            reference_code=generate_reference_code("DEP"),
            balance_after=account.balance,
        )
        create_notification(
            user=user,
            title="Deposito realizado",
            message=f"Deposito de R$ {amount} realizado na conta {account.account_number}.",
            notification_type=Notification.NotificationType.TRANSACTION,
        )
        return transaction


def withdraw(*, user, account_id: int, amount: Decimal, description: str = "") -> Transaction:
    validate_positive_amount(amount)

    with db_transaction.atomic():
        account = _get_locked_account(account_id=account_id, user=user)
        validate_sufficient_balance(balance=account.balance, amount=amount)

        account.balance -= amount
        account.save()

        transaction = Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TransactionType.WITHDRAWAL,
            amount=amount,
            description=description or "Saque realizado.",
            status=Transaction.TransactionStatus.COMPLETED,
            reference_code=generate_reference_code("WTD"),
            balance_after=account.balance,
        )
        create_notification(
            user=user,
            title="Saque realizado",
            message=f"Saque de R$ {amount} realizado na conta {account.account_number}.",
            notification_type=Notification.NotificationType.TRANSACTION,
        )
        return transaction


def transfer(
    *,
    user,
    source_account_id: int,
    destination_account_id: int,
    amount: Decimal,
    description: str = "",
) -> Transaction:
    validate_positive_amount(amount)

    if source_account_id == destination_account_id:
        raise ValidationError({"destination_account_id": "Transfer destination must be different from the source."})

    with db_transaction.atomic():
        source_account, destination_account = _get_locked_transfer_accounts(
            user=user,
            source_account_id=source_account_id,
            destination_account_id=destination_account_id,
        )
        validate_sufficient_balance(balance=source_account.balance, amount=amount)

        source_account.balance -= amount
        destination_account.balance += amount
        source_account.save()
        destination_account.save()

        outbound = Transaction.objects.create(
            account=source_account,
            destination_account=destination_account,
            transaction_type=Transaction.TransactionType.TRANSFER_OUT,
            amount=amount,
            description=description or f"Transferencia para a conta {destination_account.account_number}.",
            status=Transaction.TransactionStatus.COMPLETED,
            reference_code=generate_reference_code("TRO"),
            balance_after=source_account.balance,
        )

        Transaction.objects.create(
            account=destination_account,
            transaction_type=Transaction.TransactionType.TRANSFER_IN,
            amount=amount,
            description=description or f"Transferencia recebida da conta {source_account.account_number}.",
            status=Transaction.TransactionStatus.COMPLETED,
            reference_code=generate_reference_code("TRI"),
            balance_after=destination_account.balance,
        )
        create_notification(
            user=user,
            title="Transferencia enviada",
            message=(
                f"Transferencia de R$ {amount} enviada para a conta "
                f"{destination_account.account_number}."
            ),
            notification_type=Notification.NotificationType.TRANSACTION,
        )
        create_notification(
            user=destination_account.user,
            title="Transferencia recebida",
            message=(
                f"Transferencia de R$ {amount} recebida da conta "
                f"{source_account.account_number}."
            ),
            notification_type=Notification.NotificationType.TRANSACTION,
        )

        return outbound
