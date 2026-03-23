from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import BankAccount
from apps.investments.models import InvestmentProduct, PortfolioPosition
from apps.users.models import User


class InvestmentPositionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="carteira@ifbank.com",
            full_name="Carteira Teste",
            password="StrongPass123",
        )
        self.account = BankAccount.objects.create(
            user=self.user,
            agency_number="0001",
            account_number="555555-5",
            account_type=BankAccount.AccountType.INVESTMENT,
            balance="1500.00",
        )
        self.product = InvestmentProduct.objects.create(
            name="Produto com carencia",
            product_type=InvestmentProduct.ProductType.FIXED_INCOME,
            annual_rate="10.0000",
            minimum_initial_amount="100.00",
            term_days=30,
            risk_level=InvestmentProduct.RiskLevel.LOW,
            is_active=True,
        )
        self.old_position = PortfolioPosition.objects.create(
            account=self.account,
            product=self.product,
            invested_amount="500.00",
            current_balance="500.00",
        )
        PortfolioPosition.objects.filter(id=self.old_position.id).update(
            created_at=timezone.now() - timedelta(days=40)
        )
        self.old_position.refresh_from_db()
        self.client.force_authenticate(user=self.user)

    def test_new_application_creates_new_position_and_keeps_lock_period(self):
        apply_response = self.client.post(
            "/api/v1/investments/apply/",
            {
                "account_id": self.account.id,
                "product_id": self.product.id,
                "amount": "300.00",
            },
            format="json",
        )

        self.assertEqual(apply_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PortfolioPosition.objects.filter(account=self.account, product=self.product).count(), 2)

        new_position_id = apply_response.data["id"]
        redeem_response = self.client.post(
            "/api/v1/investments/redeem/",
            {
                "position_id": new_position_id,
                "amount": "100.00",
            },
            format="json",
        )

        self.assertEqual(redeem_response.status_code, status.HTTP_400_BAD_REQUEST)
