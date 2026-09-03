from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import get_current_usage


class CurrentUsageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        used = get_current_usage(request.user)

        try:
            limit = request.user.subscription.plan.link_limit
        except AttributeError:
            limit = 100

        remaining = None if limit is None else max(limit - used, 0)

        return Response({
            "used": used,
            "limit": limit,
            "remaining": remaining,
        })