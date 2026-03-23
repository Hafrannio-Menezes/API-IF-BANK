from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_goal_amounts(*, target_amount, current_amount):
    if current_amount > target_amount:
        raise ValidationError({"current_amount": "Current amount cannot exceed target amount."})


def validate_goal_deadline(deadline):
    if deadline <= timezone.localdate():
        raise ValidationError({"deadline": "Deadline must be a future date."})
    return deadline
