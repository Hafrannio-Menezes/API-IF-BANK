from django.shortcuts import get_object_or_404

from apps.notifications.models import Notification


def get_notifications_for_user(*, user):
    return Notification.objects.filter(user=user).order_by("-created_at")


def get_notification_for_user(*, user, notification_id: int) -> Notification:
    return get_object_or_404(Notification, id=notification_id, user=user)
