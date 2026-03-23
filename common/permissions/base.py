from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    owner_field = "user"

    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, self.owner_field, None)
        return owner == request.user
