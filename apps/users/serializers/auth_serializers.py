from rest_framework import serializers

from apps.users.serializers.profile_serializers import ProfileSerializer


class LoginInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TokenOutputSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = ProfileSerializer()
