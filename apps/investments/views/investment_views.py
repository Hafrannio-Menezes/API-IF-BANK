from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.investments.models import InvestmentProduct, InvestmentTransaction, PortfolioPosition
from apps.investments.selectors import get_active_products, get_user_investment_history, get_user_portfolio
from apps.investments.serializers import (
    ApplyInvestmentSerializer,
    InvestmentHistorySerializer,
    InvestmentProductSerializer,
    PortfolioPositionSerializer,
    RedeemInvestmentSerializer,
    SimulationInputSerializer,
    SimulationOutputSerializer,
)
from apps.investments.services import apply_investment, redeem_investment, simulate_investment


class InvestmentProductListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvestmentProductSerializer
    queryset = InvestmentProduct.objects.none()
    ordering_fields = ("name", "annual_rate", "term_days")
    search_fields = ("name", "product_type", "risk_level")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return InvestmentProduct.objects.none()
        return get_active_products()

    @extend_schema(tags=["investimentos"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PortfolioView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortfolioPositionSerializer
    queryset = PortfolioPosition.objects.none()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return PortfolioPosition.objects.none()
        return get_user_portfolio(user=self.request.user)

    @extend_schema(tags=["investimentos"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ApplyInvestmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["investimentos"], request=ApplyInvestmentSerializer, responses={201: PortfolioPositionSerializer})
    def post(self, request):
        serializer = ApplyInvestmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        position = apply_investment(user=request.user, **serializer.validated_data)
        return Response(PortfolioPositionSerializer(position).data, status=status.HTTP_201_CREATED)


class RedeemInvestmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["investimentos"], request=RedeemInvestmentSerializer, responses={200: PortfolioPositionSerializer})
    def post(self, request):
        serializer = RedeemInvestmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        position = redeem_investment(user=request.user, **serializer.validated_data)
        return Response(PortfolioPositionSerializer(position).data, status=status.HTTP_200_OK)


class InvestmentHistoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvestmentHistorySerializer
    queryset = InvestmentTransaction.objects.none()
    ordering_fields = ("created_at", "amount", "transaction_type")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return InvestmentTransaction.objects.none()
        return get_user_investment_history(user=self.request.user)

    @extend_schema(tags=["investimentos"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SimulateInvestmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["investimentos"], request=SimulationInputSerializer, responses={200: SimulationOutputSerializer})
    def post(self, request):
        serializer = SimulationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        simulation = simulate_investment(**serializer.validated_data)
        return Response(SimulationOutputSerializer(simulation).data, status=status.HTTP_200_OK)
