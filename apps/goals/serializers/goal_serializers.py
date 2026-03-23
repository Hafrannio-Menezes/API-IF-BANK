from rest_framework import serializers

from apps.goals.models import FinancialGoal
from apps.goals.validators import validate_goal_deadline
from common.serializers import CaseInsensitiveChoiceField


class GoalWriteSerializer(serializers.ModelSerializer):
    status = CaseInsensitiveChoiceField(choices=FinancialGoal.GoalStatus.choices, required=False)

    class Meta:
        model = FinancialGoal
        fields = ("title", "target_amount", "current_amount", "deadline", "status")

    def validate_deadline(self, value):
        return validate_goal_deadline(value)


class GoalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        fields = ("id", "title", "target_amount", "current_amount", "deadline", "status")


class GoalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialGoal
        fields = (
            "id",
            "title",
            "target_amount",
            "current_amount",
            "deadline",
            "status",
            "created_at",
            "updated_at",
        )
