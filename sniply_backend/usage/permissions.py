from rest_framework.permissions import BasePermission
from .services import has_quota_remaining
from rest_framework.permissions import BasePermission


class IsProUser(BasePermission):
    message = "This feature is only available on the Pro plan. Upgrade to unlock it."

    def has_permission(self, request, view):
        try:
            return request.user.subscription.plan.name == "Pro"
        except AttributeError:
            return False


class HasLinkQuotaRemaining(BasePermission):
    message = "You've reached your monthly link limit. Upgrade to Pro for unlimited links."

    def has_permission(self, request, view):
        if request.method != "POST":
            return True
        return has_quota_remaining(request.user)