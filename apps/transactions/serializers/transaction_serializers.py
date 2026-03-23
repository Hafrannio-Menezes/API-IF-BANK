from rest_framework import serializers

from apps.transactions.models import Transaction


class DepositInputSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True, max_length=255)


class WithdrawInputSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True, max_length=255)


class TransferInputSerializer(serializers.Serializer):
    source_account_id = serializers.IntegerField()
    destination_account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    description = serializers.CharField(required=False, allow_blank=True, max_length=255)


class TransactionAccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    account_number = serializers.CharField()


class TransactionSerializer(serializers.ModelSerializer):
    account = TransactionAccountSerializer(read_only=True)
    destination_account = TransactionAccountSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "account",
            "destination_account",
            "transaction_type",
            "amount",
            "description",
            "status",
            "reference_code",
            "balance_after",
            "created_at",
        )


class StatementSerializer(serializers.Serializer):
    account_id = serializers.IntegerField(required=False)
