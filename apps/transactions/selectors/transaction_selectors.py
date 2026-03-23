from apps.transactions.models import Transaction


def get_statement_queryset(*, user, account_id=None):
    queryset = Transaction.objects.select_related("account", "destination_account").filter(account__user=user)
    if account_id:
        queryset = queryset.filter(account_id=account_id)
    return queryset.order_by("-created_at")
