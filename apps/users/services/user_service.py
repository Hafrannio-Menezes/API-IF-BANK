from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.validators import normalize_email


def register_user(*, validated_data: dict) -> User:
    password = validated_data.pop("password")
    validated_data.pop("password_confirm", None)
    validated_data["email"] = normalize_email(validated_data.get("email"))

    try:
        validate_password(password=password)
    except DjangoValidationError as exc:
        raise ValidationError({"password": list(exc.messages)}) from exc

    try:
        return User.objects.create_user(password=password, **validated_data)
    except DjangoValidationError as exc:
        raise ValidationError(getattr(exc, "message_dict", {"detail": list(exc.messages)})) from exc
    except ValueError as exc:
        raise ValidationError({"detail": str(exc)}) from exc
    except IntegrityError as exc:
        raise ValidationError({"detail": "Ja existe um usuario com os dados informados."}) from exc


def authenticate_user(*, email: str, password: str) -> User:
    normalized_email = normalize_email(email)
    user = User.objects.filter(email__iexact=normalized_email).first()
    if user is None or not user.check_password(password) or not user.is_active:
        raise AuthenticationFailed("Email ou senha invalidos.")
    return user


def generate_tokens_for_user(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
