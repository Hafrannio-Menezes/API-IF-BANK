from datetime import date

from django.core.exceptions import ValidationError


PHONE_ALLOWED_CHARS = set("0123456789()-+ ")


def normalize_email(value: str | None) -> str | None:
    if not value:
        return None
    return value.strip().lower()


def validate_phone(value: str | None) -> None:
    if not value:
        return

    if any(character not in PHONE_ALLOWED_CHARS for character in value):
        raise ValidationError("Informe um numero de telefone valido.")

    digits = "".join(filter(str.isdigit, value))
    if not 10 <= len(digits) <= 13:
        raise ValidationError("Informe um numero de telefone valido.")


def validate_birth_date(value: date | None) -> None:
    if value and value > date.today():
        raise ValidationError("A data de nascimento nao pode estar no futuro.")
