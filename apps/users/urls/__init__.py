from django.urls import path

from apps.users.views import LoginView, ProfileView, PublicTokenRefreshView, RegisterView


app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", PublicTokenRefreshView.as_view(), name="token-refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
