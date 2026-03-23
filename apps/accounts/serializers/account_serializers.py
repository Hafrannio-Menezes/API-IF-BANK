from decimal import Decimal

from rest_framework import serializers

from apps.accounts.models import BankAccount
from apps.accounts.validators import validate_initial_balance
from common.serializers import CaseInsensitiveChoiceField


class AccountCreateSerializer(serializers.Serializer):
    account_type = CaseInsensitiveChoiceField(choices=BankAccount.AccountType.choices)
    initial_balance = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        required=False,
        default=Decimal("0.00"),
    )

    def validate_initial_balance(self, value):
        return validate_initial_balance(value)


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = (
            "id",
            "agency_number",
            "account_number",
            "account_type",
            "balance",
            "is_active",
            "created_at",
        )


class AccountOwnerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    email = serializers.EmailField()


class AccountDetailSerializer(serializers.ModelSerializer):
    user = AccountOwnerSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = (
            "id",
            "user",
            "agency_number",
            "account_number",
            "account_type",
            "balance",
            "is_active",
            "created_at",
            "updated_at",
        )


class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ("id", "agency_number", "account_number", "balance")
