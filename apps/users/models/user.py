from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from apps.users.models.managers import UserManager
from apps.users.validators.cpf import normalize_cpf, validate_cpf
from common.utils.models import TimeStampedModel


phone_validator = RegexValidator(
    regex=r"^\+?[0-9()\-\s]{10,20}$",
    message="Enter a valid phone number.",
)


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(
        max_length=14,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_cpf],
        help_text="Optional CPF for academic validation scenarios.",
    )
    phone = models.CharField(max_length=20, blank=True, validators=[phone_validator])
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):
        self.cpf = normalize_cpf(self.cpf)
        return super().save(*args, **kwargs)
