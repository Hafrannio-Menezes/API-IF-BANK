from rest_framework import status
from rest_framework.test import APITestCase


class PublicRoutesTests(APITestCase):
    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer token.expirado.invalido")

    def test_schema_route_is_accessible_with_invalid_authorization_header(self):
        response = self.client.get("/api/schema/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_swagger_route_is_accessible_with_invalid_authorization_header(self):
        response = self.client.get("/api/schema/swagger/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_healthcheck_route_is_accessible_with_invalid_authorization_header(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
