from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.users.models import User
from apps.users.validators import normalize_cpf, validate_birth_date, validate_phone


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "email", "cpf", "phone", "birth_date", "created_at", "updated_at")
        read_only_fields = ("id", "email", "created_at", "updated_at")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "cpf", "phone", "birth_date")

    def validate_cpf(self, value):
        user = self.instance
        normalized_value = normalize_cpf(value)
        if normalized_value and User.objects.exclude(id=user.id).filter(cpf=normalized_value).exists():
            raise serializers.ValidationError("Ja existe um usuario com este CPF.")
        return normalized_value

    def validate_phone(self, value):
        try:
            validate_phone(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages[0]) from exc
        return value

    def validate_birth_date(self, value):
        try:
            validate_birth_date(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages[0]) from exc
        return value
