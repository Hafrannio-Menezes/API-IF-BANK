from django.contrib import admin
from django.urls import include, path

from common.views import PublicSchemaView, PublicSwaggerView, healthcheck_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", healthcheck_view, name="healthcheck"),
    path("api/schema/", PublicSchemaView.as_view(), name="schema"),
    path(
        "api/schema/swagger/",
        PublicSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/v1/auth/", include("apps.users.urls")),
    path("api/v1/accounts/", include("apps.accounts.urls")),
    path("api/v1/transactions/", include("apps.transactions.urls")),
    path("api/v1/investments/", include("apps.investments.urls")),
    path("api/v1/goals/", include("apps.goals.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
]
