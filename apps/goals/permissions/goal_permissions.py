from common.permissions import IsOwner


class IsGoalOwner(IsOwner):
    owner_field = "user"
