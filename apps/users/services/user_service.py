from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


def register_user(*, validated_data: dict) -> User:
    password = validated_data.pop("password")
    validated_data.pop("password_confirm", None)

    try:
        validate_password(password=password)
    except DjangoValidationError as exc:
        raise ValidationError({"password": list(exc.messages)}) from exc

    try:
        return User.objects.create_user(password=password, **validated_data)
    except IntegrityError as exc:
        raise ValidationError({"detail": "Ja existe um usuario com os dados informados."}) from exc


def authenticate_user(*, email: str, password: str) -> User:
    user = authenticate(email=email, password=password)
    if user is None:
        raise AuthenticationFailed("Email ou senha invalidos.")
    return user


def generate_tokens_for_user(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
