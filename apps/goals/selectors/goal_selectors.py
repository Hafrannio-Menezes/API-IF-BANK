from django.shortcuts import get_object_or_404

from apps.goals.models import FinancialGoal


def get_goals_for_user(*, user):
    return FinancialGoal.objects.filter(user=user).order_by("deadline", "-created_at")


def get_goal_for_user(*, user, goal_id: int) -> FinancialGoal:
    return get_object_or_404(FinancialGoal, id=goal_id, user=user)
