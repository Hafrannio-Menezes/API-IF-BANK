from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.goals.models import FinancialGoal
from apps.users.models import User


class GoalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="meta@ifbank.com",
            full_name="Meta User",
            password="StrongPass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_user_can_create_goal(self):
        response = self.client.post(
            "/api/v1/goals/",
            {
                "title": "Reserva de emergencia",
                "target_amount": "10000.00",
                "current_amount": "1500.00",
                "deadline": (timezone.localdate() + timedelta(days=120)).isoformat(),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FinancialGoal.objects.count(), 1)
        self.assertEqual(FinancialGoal.objects.first().status, FinancialGoal.GoalStatus.ACTIVE)

    def test_user_can_create_goal_with_lowercase_status(self):
        response = self.client.post(
            "/api/v1/goals/",
            {
                "title": "Meta pausada",
                "target_amount": "5000.00",
                "current_amount": "1000.00",
                "deadline": (timezone.localdate() + timedelta(days=90)).isoformat(),
                "status": "cancelled",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FinancialGoal.objects.count(), 1)
        self.assertEqual(FinancialGoal.objects.first().status, FinancialGoal.GoalStatus.CANCELLED)
