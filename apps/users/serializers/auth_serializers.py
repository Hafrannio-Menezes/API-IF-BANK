from rest_framework import serializers

from apps.users.serializers.profile_serializers import ProfileSerializer
from apps.users.validators import normalize_email


class LoginInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        return normalize_email(value)


class TokenOutputSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = ProfileSerializer()
