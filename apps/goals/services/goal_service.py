from apps.goals.models import FinancialGoal
from apps.notifications.models import Notification
from apps.notifications.services import create_notification
from apps.goals.validators import validate_goal_amounts


def _resolve_status(*, current_amount, target_amount, provided_status=None):
    if provided_status == FinancialGoal.GoalStatus.CANCELLED:
        return FinancialGoal.GoalStatus.CANCELLED
    if current_amount >= target_amount:
        return FinancialGoal.GoalStatus.ACHIEVED
    return FinancialGoal.GoalStatus.ACTIVE


def create_goal(*, user, validated_data: dict) -> FinancialGoal:
    validate_goal_amounts(
        target_amount=validated_data["target_amount"],
        current_amount=validated_data.get("current_amount", 0),
    )
    validated_data["status"] = _resolve_status(
        current_amount=validated_data.get("current_amount", 0),
        target_amount=validated_data["target_amount"],
        provided_status=validated_data.get("status"),
    )
    goal = FinancialGoal.objects.create(user=user, **validated_data)
    create_notification(
        user=user,
        title="Meta criada",
        message=f"Meta '{goal.title}' criada com sucesso.",
        notification_type=Notification.NotificationType.GOAL,
    )
    return goal


def update_goal(*, goal: FinancialGoal, validated_data: dict) -> FinancialGoal:
    target_amount = validated_data.get("target_amount", goal.target_amount)
    current_amount = validated_data.get("current_amount", goal.current_amount)
    validate_goal_amounts(target_amount=target_amount, current_amount=current_amount)

    for field, value in validated_data.items():
        setattr(goal, field, value)

    goal.status = _resolve_status(
        current_amount=current_amount,
        target_amount=target_amount,
        provided_status=validated_data.get("status", goal.status),
    )
    goal.save()
    create_notification(
        user=goal.user,
        title="Meta atualizada",
        message=f"Meta '{goal.title}' atualizada com sucesso.",
        notification_type=Notification.NotificationType.GOAL,
    )
    return goal
