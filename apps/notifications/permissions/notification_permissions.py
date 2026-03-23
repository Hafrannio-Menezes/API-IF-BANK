from common.permissions import IsOwner


class IsNotificationOwner(IsOwner):
    owner_field = "user"
