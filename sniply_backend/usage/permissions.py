from rest_framework.permissions import BasePermission
from .services import has_quota_remaining


class HasLinkQuotaRemaining(BasePermission):
    message = "You've reached your monthly link limit. Upgrade to Pro for unlimited links."

    def has_permission(self, request, view):
        if request.method != "POST":
            return True
        return has_quota_remaining(request.user)