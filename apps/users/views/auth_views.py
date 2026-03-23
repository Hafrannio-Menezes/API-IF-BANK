from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.throttling import AuthRateThrottle
from apps.users.serializers import (
    LoginInputSerializer,
    ProfileSerializer,
    RegisterInputSerializer,
    RegisterOutputSerializer,
    RegisterResponseSerializer,
    TokenOutputSerializer,
)
from apps.users.services.user_service import authenticate_user, generate_tokens_for_user, register_user


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AuthRateThrottle]

    @extend_schema(
        tags=["autenticacao"],
        request=RegisterInputSerializer,
        responses={201: RegisterResponseSerializer},
        examples=[
            OpenApiExample(
                "solicitacao de cadastro",
                value={
                    "full_name": "Maria Souza",
                    "email": "maria@ifbank.com",
                    "password": "StrongPass123",
                    "password_confirm": "StrongPass123",
                    "cpf": "39053344705",
                    "phone": "+55 11 99999-9999",
                    "birth_date": "1998-04-10",
                },
                request_only=True,
            )
        ],
    )
    def post(self, request):
        serializer = RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = register_user(validated_data=serializer.validated_data)
        data = RegisterOutputSerializer(user).data
        data["tokens"] = generate_tokens_for_user(user)
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AuthRateThrottle]

    @extend_schema(
        tags=["autenticacao"],
        request=LoginInputSerializer,
        responses={200: TokenOutputSerializer},
    )
    def post(self, request):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate_user(**serializer.validated_data)
        return Response(
            {
                **generate_tokens_for_user(user),
                "user": ProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
