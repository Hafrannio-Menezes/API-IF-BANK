from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.goals.models import FinancialGoal
from apps.goals.permissions import IsGoalOwner
from apps.goals.selectors import get_goal_for_user, get_goals_for_user
from apps.goals.serializers import GoalDetailSerializer, GoalListSerializer, GoalWriteSerializer
from apps.goals.services import create_goal, update_goal


class GoalListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = FinancialGoal.objects.none()
    ordering_fields = ("deadline", "target_amount", "current_amount", "created_at")
    search_fields = ("title", "status")

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return FinancialGoal.objects.none()
        return get_goals_for_user(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return GoalWriteSerializer
        return GoalListSerializer

    @extend_schema(tags=["metas"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["metas"], responses={201: GoalDetailSerializer})
    def post(self, request, *args, **kwargs):
        serializer = GoalWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        goal = create_goal(user=request.user, validated_data=serializer.validated_data)
        return Response(GoalDetailSerializer(goal).data, status=status.HTTP_201_CREATED)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsGoalOwner]
    serializer_class = GoalDetailSerializer

    def get_object(self):
        goal = get_goal_for_user(user=self.request.user, goal_id=self.kwargs["goal_id"])
        self.check_object_permissions(self.request, goal)
        return goal

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return GoalWriteSerializer
        return GoalDetailSerializer

    @extend_schema(tags=["metas"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(tags=["metas"], responses={200: GoalDetailSerializer})
    def patch(self, request, *args, **kwargs):
        goal = self.get_object()
        serializer = GoalWriteSerializer(goal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_goal = update_goal(goal=goal, validated_data=serializer.validated_data)
        return Response(GoalDetailSerializer(updated_goal).data)

    @extend_schema(tags=["metas"], responses={200: GoalDetailSerializer})
    def put(self, request, *args, **kwargs):
        goal = self.get_object()
        serializer = GoalWriteSerializer(goal, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_goal = update_goal(goal=goal, validated_data=serializer.validated_data)
        return Response(GoalDetailSerializer(updated_goal).data)
