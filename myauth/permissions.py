from rest_framework.permissions import BasePermission


class IsAdminAuthenticated(BasePermission):
    """
    Permission for logged in Admin.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )


class IsOwner(BasePermission):
    """
    Permission for logged user, used to allow a user to modify its own
    data.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user
