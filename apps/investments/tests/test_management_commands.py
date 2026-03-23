from django.core.management import call_command
from django.test import TestCase

from apps.investments.models import InvestmentProduct


class SyncInvestmentProductsCommandTests(TestCase):
    def test_command_loads_reference_products(self):
        InvestmentProduct.objects.all().delete()

        call_command("sync_investment_products")

        self.assertEqual(InvestmentProduct.objects.count(), 4)
        self.assertTrue(InvestmentProduct.objects.filter(name="CDB Liquidez Diaria").exists())

    def test_command_is_idempotent(self):
        call_command("sync_investment_products")
        call_command("sync_investment_products")

        self.assertEqual(InvestmentProduct.objects.count(), 4)
