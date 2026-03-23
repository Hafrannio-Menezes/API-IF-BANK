from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import permissions


class PublicSchemaView(SpectacularAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]


class PublicSwaggerView(SpectacularSwaggerView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
