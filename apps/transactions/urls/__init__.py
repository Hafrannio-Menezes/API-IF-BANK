from django.urls import path

from apps.transactions.views import DepositView, StatementView, TransferView, WithdrawView


app_name = "transactions"

urlpatterns = [
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("withdraw/", WithdrawView.as_view(), name="withdraw"),
    path("transfer/", TransferView.as_view(), name="transfer"),
    path("statement/", StatementView.as_view(), name="statement"),
]
