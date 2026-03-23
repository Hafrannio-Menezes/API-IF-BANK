from decimal import Decimal

from rest_framework import serializers

from apps.investments.models import InvestmentProduct, InvestmentTransaction, PortfolioPosition


class InvestmentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentProduct
        fields = (
            "id",
            "name",
            "product_type",
            "annual_rate",
            "minimum_initial_amount",
            "term_days",
            "risk_level",
            "description",
            "is_active",
        )


class PortfolioAccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    account_number = serializers.CharField()
    agency_number = serializers.CharField()


class PortfolioPositionSerializer(serializers.ModelSerializer):
    product = InvestmentProductSerializer()
    account = PortfolioAccountSerializer(read_only=True)

    class Meta:
        model = PortfolioPosition
        fields = (
            "id",
            "account",
            "product",
            "invested_amount",
            "current_balance",
            "created_at",
            "updated_at",
        )


class InvestmentHistorySerializer(serializers.ModelSerializer):
    position = PortfolioPositionSerializer()

    class Meta:
        model = InvestmentTransaction
        fields = ("id", "position", "transaction_type", "amount", "reference_code", "created_at")


class ApplyInvestmentSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)


class RedeemInvestmentSerializer(serializers.Serializer):
    position_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)


class SimulationInputSerializer(serializers.Serializer):
    initial_amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    annual_rate = serializers.DecimalField(max_digits=7, decimal_places=4)
    period_months = serializers.IntegerField(min_value=1)
    monthly_contribution = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        required=False,
        default=Decimal("0.00"),
    )

    def to_internal_value(self, data):
        normalized_data = data.copy() if hasattr(data, "copy") else dict(data)
        if "monthly_contribution" not in normalized_data and "monthly_amount" in normalized_data:
            normalized_data["monthly_contribution"] = normalized_data["monthly_amount"]
        return super().to_internal_value(normalized_data)


class SimulationOutputSerializer(serializers.Serializer):
    initial_amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    annual_rate = serializers.DecimalField(max_digits=7, decimal_places=4)
    period_months = serializers.IntegerField()
    monthly_contribution = serializers.DecimalField(max_digits=14, decimal_places=2)
    invested_capital = serializers.DecimalField(max_digits=14, decimal_places=2)
    estimated_return = serializers.DecimalField(max_digits=14, decimal_places=2)
    final_amount = serializers.DecimalField(max_digits=14, decimal_places=2)
