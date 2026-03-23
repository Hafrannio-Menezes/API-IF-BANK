from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import BankAccount
from apps.users.models import User


class TransactionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="finance@ifbank.com",
            full_name="Finance User",
            password="StrongPass123",
        )
        self.destination_user = User.objects.create_user(
            email="destino@ifbank.com",
            full_name="Destino User",
            password="StrongPass123",
        )
        self.source_account = BankAccount.objects.create(
            user=self.user,
            agency_number="0001",
            account_number="123456-1",
            account_type=BankAccount.AccountType.CHECKING,
            balance="1000.00",
        )
        self.destination_account = BankAccount.objects.create(
            user=self.destination_user,
            agency_number="0001",
            account_number="654321-9",
            account_type=BankAccount.AccountType.SAVINGS,
            balance="500.00",
        )
        self.client.force_authenticate(user=self.user)

    def test_deposit_increases_balance(self):
        response = self.client.post(
            "/api/v1/transactions/deposit/",
            {"account_id": self.source_account.id, "amount": "200.00"},
            format="json",
        )

        self.source_account.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(self.source_account.balance), "1200.00")

    def test_withdraw_decreases_balance(self):
        response = self.client.post(
            "/api/v1/transactions/withdraw/",
            {"account_id": self.source_account.id, "amount": "150.00"},
            format="json",
        )

        self.source_account.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(self.source_account.balance), "850.00")

    def test_transfer_moves_amount_between_accounts(self):
        response = self.client.post(
            "/api/v1/transactions/transfer/",
            {
                "source_account_id": self.source_account.id,
                "destination_account_id": self.destination_account.id,
                "amount": "300.00",
            },
            format="json",
        )

        self.source_account.refresh_from_db()
        self.destination_account.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(self.source_account.balance), "700.00")
        self.assertEqual(str(self.destination_account.balance), "800.00")
