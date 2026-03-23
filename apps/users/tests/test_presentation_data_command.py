from django.core.management import call_command
from django.test import TestCase

from apps.accounts.models import BankAccount
from apps.goals.models import FinancialGoal
from apps.investments.models import PortfolioPosition
from apps.transactions.models import Transaction
from apps.users.models import User


class LoadPresentationDataCommandTests(TestCase):
    def test_command_creates_presentation_dataset(self):
        call_command("load_presentation_data")

        self.assertEqual(User.objects.filter(email__endswith="@ifbank.local").count(), 2)
        self.assertEqual(BankAccount.objects.count(), 2)
        self.assertEqual(FinancialGoal.objects.count(), 2)
        self.assertEqual(PortfolioPosition.objects.count(), 1)
        self.assertGreaterEqual(Transaction.objects.count(), 6)

    def test_command_can_be_executed_twice_without_duplicate_demo_records(self):
        call_command("load_presentation_data")
        call_command("load_presentation_data")

        self.assertEqual(User.objects.filter(email__endswith="@ifbank.local").count(), 2)
        self.assertEqual(BankAccount.objects.count(), 2)
        self.assertEqual(FinancialGoal.objects.count(), 2)
