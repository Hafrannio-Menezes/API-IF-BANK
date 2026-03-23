from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class SimulationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="invest@ifbank.com",
            full_name="Investidor",
            password="StrongPass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_can_simulate_investment(self):
        response = self.client.post(
            "/api/v1/investments/simulate/",
            {
                "initial_amount": "1000.00",
                "annual_rate": "12.00",
                "period_months": 12,
                "monthly_contribution": "100.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("final_amount", response.data)
        self.assertGreater(float(response.data["final_amount"]), 0)

    def test_authenticated_user_can_simulate_investment_with_alias_and_default_contribution(self):
        response = self.client.post(
            "/api/v1/investments/simulate/",
            {
                "initial_amount": "1000.00",
                "annual_rate": "12.00",
                "period_months": 12,
                "monthly_amount": "50.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["monthly_contribution"], "50.00")
