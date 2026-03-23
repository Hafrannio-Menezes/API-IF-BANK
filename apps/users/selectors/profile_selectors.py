from apps.users.models import User


def get_user_profile(user_id: int) -> User:
    return User.objects.get(id=user_id)
