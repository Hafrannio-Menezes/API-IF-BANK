from django.shortcuts import get_object_or_404

from apps.investments.models import InvestmentProduct, InvestmentTransaction, PortfolioPosition


def get_active_products():
    return InvestmentProduct.objects.filter(is_active=True).order_by("name")


def get_user_portfolio(*, user):
    return PortfolioPosition.objects.select_related("product", "account").filter(account__user=user).order_by("-created_at")


def get_position_for_user(*, user, position_id: int) -> PortfolioPosition:
    return get_object_or_404(PortfolioPosition.objects.select_related("product", "account"), id=position_id, account__user=user)


def get_user_investment_history(*, user):
    return (
        InvestmentTransaction.objects.select_related("position", "position__product", "position__account")
        .filter(position__account__user=user)
        .order_by("-created_at")
    )
