from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import BankAccount
from apps.transactions.models import Transaction
from apps.users.models import User


class AccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="conta@ifbank.com",
            full_name="Conta Teste",
            password="StrongPass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_authenticated_user_can_create_account(self):
        response = self.client.post(
            "/api/v1/accounts/",
            {"account_type": BankAccount.AccountType.CHECKING, "initial_balance": "1000.00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BankAccount.objects.count(), 1)
        self.assertEqual(str(BankAccount.objects.first().balance), "1000.00")
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.first().transaction_type, Transaction.TransactionType.DEPOSIT)

    def test_authenticated_user_can_create_account_with_lowercase_type_and_default_balance(self):
        response = self.client.post(
            "/api/v1/accounts/",
            {"account_type": "checking"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BankAccount.objects.count(), 1)
        self.assertEqual(str(BankAccount.objects.first().balance), "0.00")
        self.assertEqual(Transaction.objects.count(), 0)
