import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.db import transaction as db_transaction

from apps.accounts.services import create_account
from apps.goals.services import create_goal
from apps.investments.models import InvestmentProduct
from apps.investments.services import apply_investment, sync_investment_products
from apps.transactions.services import deposit, transfer, withdraw
from apps.users.models import User


PRESENTATION_DATA_FILE = Path(settings.BASE_DIR) / "data" / "demo" / "presentation_data.json"


def _load_presentation_payload(data_file: Path | None = None) -> dict:
    file_path = data_file or PRESENTATION_DATA_FILE
    with file_path.open(encoding="utf-8") as file_handler:
        return json.load(file_handler)


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def _reset_presentation_users(payload: dict) -> None:
    emails = [user_payload["email"] for user_payload in payload.get("users", [])]
    if emails:
        User.objects.filter(email__in=emails).delete()


def load_presentation_data(*, data_file: Path | None = None, reset_existing: bool = True) -> dict:
    payload = _load_presentation_payload(data_file=data_file)
    sync_investment_products()

    summary = {
        "users": 0,
        "accounts": 0,
        "goals": 0,
        "transfers": 0,
        "investments": 0,
    }

    with db_transaction.atomic():
        if reset_existing:
            _reset_presentation_users(payload)

        accounts_by_key = {}

        for user_payload in payload.get("users", []):
            user = User.objects.create_user(
                email=user_payload["email"],
                full_name=user_payload["full_name"],
                password=user_payload["password"],
                cpf=user_payload.get("cpf"),
                phone=user_payload.get("phone", ""),
                birth_date=_parse_date(user_payload.get("birth_date")),
            )
            summary["users"] += 1

            for account_payload in user_payload.get("accounts", []):
                account = create_account(
                    user=user,
                    validated_data={
                        "account_type": account_payload["account_type"],
                        "initial_balance": Decimal(account_payload.get("initial_balance", "0.00")),
                    },
                )
                accounts_by_key[account_payload["key"]] = account
                summary["accounts"] += 1

                for operation_payload in account_payload.get("operations", []):
                    operation_type = operation_payload["type"]
                    operation_amount = Decimal(operation_payload["amount"])
                    operation_description = operation_payload.get("description", "")

                    if operation_type == "deposit":
                        deposit(
                            user=user,
                            account_id=account.id,
                            amount=operation_amount,
                            description=operation_description,
                        )
                    elif operation_type == "withdraw":
                        withdraw(
                            user=user,
                            account_id=account.id,
                            amount=operation_amount,
                            description=operation_description,
                        )

            for goal_payload in user_payload.get("goals", []):
                create_goal(
                    user=user,
                    validated_data={
                        "title": goal_payload["title"],
                        "target_amount": Decimal(goal_payload["target_amount"]),
                        "current_amount": Decimal(goal_payload.get("current_amount", "0.00")),
                        "deadline": _parse_date(goal_payload["deadline"]),
                        "status": goal_payload.get("status"),
                    },
                )
                summary["goals"] += 1

        for transfer_payload in payload.get("transfers", []):
            source_account = accounts_by_key[transfer_payload["from_account"]]
            destination_account = accounts_by_key[transfer_payload["to_account"]]
            transfer(
                user=source_account.user,
                source_account_id=source_account.id,
                destination_account_id=destination_account.id,
                amount=Decimal(transfer_payload["amount"]),
                description=transfer_payload.get("description", ""),
            )
            summary["transfers"] += 1

        for investment_payload in payload.get("investments", []):
            account = accounts_by_key[investment_payload["account"]]
            product = InvestmentProduct.objects.get(name=investment_payload["product_name"], is_active=True)
            apply_investment(
                user=account.user,
                account_id=account.id,
                product_id=product.id,
                amount=Decimal(investment_payload["amount"]),
            )
            summary["investments"] += 1

    return summary
