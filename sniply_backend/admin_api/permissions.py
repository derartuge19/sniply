from rest_framework.permissions import BasePermission


class IsStaffOnly(BasePermission):
    message = "You do not have permission to access this resource."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff