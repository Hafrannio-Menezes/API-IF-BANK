from django.contrib.auth.base_user import BaseUserManager

from apps.users.validators import normalize_email


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Um email e obrigatorio.")

        email = normalize_email(email)
        if self.model.objects.filter(email__iexact=email).exists():
            raise ValueError("Ja existe um usuario com este email.")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuario precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuario precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
