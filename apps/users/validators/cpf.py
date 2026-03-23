from django.core.exceptions import ValidationError


def normalize_cpf(value: str | None) -> str | None:
    if not value:
        return None

    digits = "".join(filter(str.isdigit, value))
    return digits or None


def validate_cpf(value: str) -> None:
    digits = normalize_cpf(value)
    if not digits:
        return

    if len(digits) != 11 or len(set(digits)) == 1:
        raise ValidationError("CPF must contain 11 valid digits.")

    for size in (9, 10):
        total = sum(int(digits[index]) * ((size + 1) - index) for index in range(size))
        remainder = (total * 10) % 11
        check_digit = 0 if remainder == 10 else remainder
        if check_digit != int(digits[size]):
            raise ValidationError("CPF is invalid.")
