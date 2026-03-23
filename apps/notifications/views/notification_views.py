from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.notifications.models import Notification
from apps.notifications.permissions import IsNotificationOwner
from apps.notifications.selectors import get_notification_for_user, get_notifications_for_user
from apps.notifications.serializers import NotificationListSerializer
from apps.notifications.services import mark_notification_as_read


class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationListSerializer
    queryset = Notification.objects.none()
    ordering_fields = ("created_at", "is_read", "notification_type")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.queryset
        return get_notifications_for_user(user=self.request.user)

    @extend_schema(tags=["notificacoes"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class NotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsNotificationOwner]
    serializer_class = NotificationListSerializer

    @extend_schema(tags=["notificacoes"], responses={200: NotificationListSerializer})
    def post(self, request, notification_id: int):
        notification = get_notification_for_user(user=request.user, notification_id=notification_id)
        self.check_object_permissions(request, notification)
        notification = mark_notification_as_read(notification=notification)
        return Response(NotificationListSerializer(notification).data)
