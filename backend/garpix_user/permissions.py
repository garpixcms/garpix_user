from rest_framework.permissions import BasePermission


class IsUnAuthenticated(BasePermission):
    """
    Allows access only to not authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_authenticated)
