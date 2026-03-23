from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.users.models import User
from apps.users.validators import normalize_cpf, normalize_email, validate_birth_date, validate_phone


class RegisterInputSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    cpf = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=14)
    phone = serializers.CharField(required=False, allow_blank=True, max_length=20)
    birth_date = serializers.DateField(required=False, allow_null=True)

    def validate_email(self, value):
        normalized_value = normalize_email(value)
        if User.objects.filter(email__iexact=normalized_value).exists():
            raise serializers.ValidationError("Ja existe um usuario com este email.")
        return normalized_value

    def validate_cpf(self, value):
        normalized_value = normalize_cpf(value)
        if normalized_value and User.objects.filter(cpf=normalized_value).exists():
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

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "As senhas nao coincidem."})
        return attrs


class RegisterOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "full_name", "email", "cpf", "phone", "birth_date", "created_at", "updated_at")


class RegisterResponseSerializer(RegisterOutputSerializer):
    tokens = serializers.DictField(child=serializers.CharField())

    class Meta(RegisterOutputSerializer.Meta):
        fields = RegisterOutputSerializer.Meta.fields + ("tokens",)
