from django.contrib import admin

from apps.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "notification_type", "is_read", "created_at")
    search_fields = ("title", "message", "user__email", "user__full_name")
    list_filter = ("notification_type", "is_read", "created_at")
    readonly_fields = ("created_at",)
