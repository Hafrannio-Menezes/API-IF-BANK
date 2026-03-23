from rest_framework import status
from rest_framework.test import APITestCase

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
