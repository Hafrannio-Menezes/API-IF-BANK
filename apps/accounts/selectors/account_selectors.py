from django.shortcuts import get_object_or_404

from apps.accounts.models import BankAccount


def get_user_accounts(user):
    return BankAccount.objects.filter(user=user).order_by("-created_at")


def get_user_account(*, user, account_id: int) -> BankAccount:
    return get_object_or_404(BankAccount, id=account_id, user=user)
