from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from apps.users.permissions import IsSelfUser
from apps.users.serializers import ProfileSerializer, ProfileUpdateSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSelfUser]

    def get_object(self):
        user = self.request.user
        self.check_object_permissions(self.request, user)
        return user

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProfileUpdateSerializer
        return ProfileSerializer

    @extend_schema(tags=["autenticacao"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["autenticacao"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(tags=["autenticacao"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
