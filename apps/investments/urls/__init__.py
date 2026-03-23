from django.urls import path

from apps.investments.views import (
    ApplyInvestmentView,
    InvestmentHistoryView,
    InvestmentProductListView,
    PortfolioView,
    RedeemInvestmentView,
    SimulateInvestmentView,
)


app_name = "investments"

urlpatterns = [
    path("products/", InvestmentProductListView.as_view(), name="products"),
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    path("apply/", ApplyInvestmentView.as_view(), name="apply"),
    path("redeem/", RedeemInvestmentView.as_view(), name="redeem"),
    path("history/", InvestmentHistoryView.as_view(), name="history"),
    path("simulate/", SimulateInvestmentView.as_view(), name="simulate"),
]
