from django.urls import path

from apps.accounts.views import AccountBalanceView, AccountDetailView, AccountListCreateView


app_name = "accounts"

urlpatterns = [
    path("", AccountListCreateView.as_view(), name="account-list-create"),
    path("<int:account_id>/", AccountDetailView.as_view(), name="account-detail"),
    path("<int:account_id>/balance/", AccountBalanceView.as_view(), name="account-balance"),
]
