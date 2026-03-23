from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.transactions.models import Transaction
from apps.transactions.selectors import get_statement_queryset
from apps.transactions.serializers import (
    DepositInputSerializer,
    StatementSerializer,
    TransferInputSerializer,
    TransactionSerializer,
    WithdrawInputSerializer,
)
from apps.transactions.services import deposit, transfer, withdraw


class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["transacoes"], request=DepositInputSerializer, responses={201: TransactionSerializer})
    def post(self, request):
        serializer = DepositInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = deposit(user=request.user, **serializer.validated_data)
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


class WithdrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["transacoes"], request=WithdrawInputSerializer, responses={201: TransactionSerializer})
    def post(self, request):
        serializer = WithdrawInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = withdraw(user=request.user, **serializer.validated_data)
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


class TransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["transacoes"], request=TransferInputSerializer, responses={201: TransactionSerializer})
    def post(self, request):
        serializer = TransferInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = transfer(user=request.user, **serializer.validated_data)
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


class StatementView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.none()
    ordering_fields = ("created_at", "amount", "transaction_type")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Transaction.objects.none()
        query_serializer = StatementSerializer(data=self.request.query_params)
        query_serializer.is_valid(raise_exception=True)
        return get_statement_queryset(user=self.request.user, **query_serializer.validated_data)

    @extend_schema(tags=["transacoes"], parameters=[StatementSerializer])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
