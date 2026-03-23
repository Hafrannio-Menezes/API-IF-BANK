from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import BankAccount
from apps.accounts.permissions import IsAccountOwner
from apps.accounts.selectors import get_user_account, get_user_accounts
from apps.accounts.serializers import (
    AccountBalanceSerializer,
    AccountCreateSerializer,
    AccountDetailSerializer,
    AccountListSerializer,
)
from apps.accounts.services import create_account


class AccountListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BankAccount.objects.none()
    ordering_fields = ("created_at", "balance", "account_type")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return BankAccount.objects.none()
        return get_user_accounts(self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AccountCreateSerializer
        return AccountListSerializer

    @extend_schema(tags=["contas"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["contas"], responses={201: AccountDetailSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = create_account(user=request.user, validated_data=serializer.validated_data)
        return Response(AccountDetailSerializer(account).data, status=status.HTTP_201_CREATED)


class AccountDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]
    serializer_class = AccountDetailSerializer

    def get_object(self):
        account = get_user_account(user=self.request.user, account_id=self.kwargs["account_id"])
        self.check_object_permissions(self.request, account)
        return account

    @extend_schema(tags=["contas"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AccountBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAccountOwner]

    @extend_schema(tags=["contas"], responses={200: AccountBalanceSerializer})
    def get(self, request, account_id: int):
        account = get_user_account(user=request.user, account_id=account_id)
        self.check_object_permissions(request, account)
        return Response(AccountBalanceSerializer(account).data)
