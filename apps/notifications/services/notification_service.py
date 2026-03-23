from apps.notifications.models import Notification


def create_notification(*, user, title: str, message: str, notification_type: str) -> Notification:
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
    )


def mark_notification_as_read(*, notification: Notification) -> Notification:
    notification.is_read = True
    notification.save(update_fields=["is_read"])
    return notification
