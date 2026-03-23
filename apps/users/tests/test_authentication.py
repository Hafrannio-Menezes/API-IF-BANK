from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


class AuthenticationTests(APITestCase):
    def test_user_can_register(self):
        payload = {
            "full_name": "Maria Souza",
            "email": "maria@ifbank.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
            "cpf": "39053344705",
        }

        response = self.client.post("/api/v1/auth/register/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=payload["email"]).exists())
        self.assertIn("access", response.data["tokens"])

    def test_user_can_login(self):
        user = User.objects.create_user(
            email="joao@ifbank.com",
            full_name="Joao Silva",
            password="StrongPass123",
        )

        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": user.email, "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_can_login_even_with_invalid_authorization_header(self):
        user = User.objects.create_user(
            email="header@ifbank.com",
            full_name="Header Teste",
            password="StrongPass123",
        )
        self.client.credentials(HTTP_AUTHORIZATION="Bearer token.expirado.invalido")

        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": user.email, "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_can_register_even_with_invalid_authorization_header(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer token.expirado.invalido")
        payload = {
            "full_name": "Registro Header",
            "email": "registro.header@ifbank.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
        }

        response = self.client.post("/api/v1/auth/register/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=payload["email"]).exists())

    def test_user_can_refresh_token_even_with_invalid_authorization_header(self):
        user = User.objects.create_user(
            email="refresh.header@ifbank.com",
            full_name="Refresh Header",
            password="StrongPass123",
        )
        refresh = str(RefreshToken.for_user(user))
        self.client.credentials(HTTP_AUTHORIZATION="Bearer token.expirado.invalido")

        response = self.client.post(
            "/api/v1/auth/refresh/",
            {"refresh": refresh},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_register_normalizes_email_and_blocks_case_insensitive_duplicate(self):
        first_payload = {
            "full_name": "Case One",
            "email": "User@Test.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
        }
        second_payload = {
            "full_name": "Case Two",
            "email": "user@Test.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
        }

        first_response = self.client.post("/api/v1/auth/register/", first_payload, format="json")
        second_response = self.client.post("/api/v1/auth/register/", second_payload, format="json")

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(email="user@test.com").exists())

    def test_user_can_login_with_email_in_different_case(self):
        User.objects.create_user(
            email="Case.Login@Test.com",
            full_name="Case Login",
            password="StrongPass123",
        )

        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": "CASE.LOGIN@test.COM", "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_register_rejects_invalid_phone(self):
        payload = {
            "full_name": "Telefone Invalido",
            "email": "telefone@ifbank.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
            "phone": "((((((((((",
        }

        response = self.client.post("/api/v1/auth/register/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data["errors"])

    def test_register_rejects_future_birth_date(self):
        payload = {
            "full_name": "Nascimento Futuro",
            "email": "nascimento@ifbank.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
            "birth_date": "2099-01-01",
        }

        response = self.client.post("/api/v1/auth/register/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birth_date", response.data["errors"])

    def test_two_users_can_register_with_blank_cpf(self):
        first_payload = {
            "full_name": "Primeiro Usuario",
            "email": "primeiro@ifbank.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
            "cpf": "",
        }
        second_payload = {
            "full_name": "Segundo Usuario",
            "email": "segundo@ifbank.com",
            "password": "StrongPass123",
            "password_confirm": "StrongPass123",
            "cpf": "",
        }

        first_response = self.client.post("/api/v1/auth/register/", first_payload, format="json")
        second_response = self.client.post("/api/v1/auth/register/", second_payload, format="json")

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(cpf__isnull=True).count(), 2)


class ProfileValidationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="perfil@ifbank.com",
            full_name="Perfil Teste",
            password="StrongPass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_profile_update_rejects_invalid_phone(self):
        response = self.client.patch(
            "/api/v1/auth/profile/",
            {"phone": "(((((((((("},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data["errors"])

    def test_profile_update_rejects_future_birth_date(self):
        response = self.client.patch(
            "/api/v1/auth/profile/",
            {"birth_date": "2099-01-01"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birth_date", response.data["errors"])
