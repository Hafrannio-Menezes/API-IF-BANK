from django.urls import path

from apps.goals.views import GoalDetailView, GoalListCreateView


app_name = "goals"

urlpatterns = [
    path("", GoalListCreateView.as_view(), name="goal-list-create"),
    path("<int:goal_id>/", GoalDetailView.as_view(), name="goal-detail"),
]
