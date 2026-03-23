from decimal import Decimal

from django.db import transaction as db_transaction

from apps.accounts.models import BankAccount
from apps.notifications.models import Notification
from apps.notifications.services import create_notification
from apps.transactions.models import Transaction
from common.utils.identifiers import generate_account_number, generate_agency_number
from common.utils.identifiers import generate_reference_code


def _generate_unique_account_number() -> str:
    account_number = generate_account_number()
    while BankAccount.objects.filter(account_number=account_number).exists():
        account_number = generate_account_number()
    return account_number


def create_account(*, user, validated_data: dict) -> BankAccount:
    initial_balance = validated_data.pop("initial_balance", 0)
    with db_transaction.atomic():
        account = BankAccount.objects.create(
            user=user,
            agency_number=generate_agency_number(),
            account_number=_generate_unique_account_number(),
            balance=initial_balance,
            **validated_data,
        )

        if initial_balance > Decimal("0"):
            Transaction.objects.create(
                account=account,
                transaction_type=Transaction.TransactionType.DEPOSIT,
                amount=initial_balance,
                description="Saldo inicial da conta.",
                status=Transaction.TransactionStatus.COMPLETED,
                reference_code=generate_reference_code("DEP"),
                balance_after=account.balance,
            )

        create_notification(
            user=user,
            title="Conta criada",
            message=f"Conta {account.account_number} criada com sucesso.",
            notification_type=Notification.NotificationType.ACCOUNT,
        )
        return account
