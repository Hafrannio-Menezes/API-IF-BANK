from common.permissions import IsOwner


class IsAccountOwner(IsOwner):
    owner_field = "user"
