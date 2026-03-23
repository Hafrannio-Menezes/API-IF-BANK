from django.db import models
from django.db.models import Q

from common.utils.models import TimeStampedModel


class InvestmentProduct(TimeStampedModel):
    class ProductType(models.TextChoices):
        CDB = "CDB", "CDB"
        CDI_FUND = "CDI_FUND", "CDI Fund"
        TESOURO = "TESOURO", "Tesouro Direto"
        LCI = "LCI", "LCI"
        FIXED_INCOME = "FIXED_INCOME", "Fixed Income"

    class RiskLevel(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    name = models.CharField(max_length=150, unique=True)
    product_type = models.CharField(max_length=20, choices=ProductType.choices)
    annual_rate = models.DecimalField(max_digits=7, decimal_places=4)
    minimum_initial_amount = models.DecimalField(max_digits=14, decimal_places=2)
    term_days = models.PositiveIntegerField(default=30)
    risk_level = models.CharField(max_length=10, choices=RiskLevel.choices)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(check=Q(annual_rate__gte=0), name="investments_product_annual_rate_non_negative"),
            models.CheckConstraint(
                check=Q(minimum_initial_amount__gt=0),
                name="investments_product_minimum_initial_amount_positive",
            ),
        ]
        verbose_name = "Investment product"
        verbose_name_plural = "Investment products"

    def __str__(self) -> str:
        return self.name
