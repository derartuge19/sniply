from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import get_current_usage, FREE_TIER_LIMIT


class CurrentUsageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        used = get_current_usage(request.user)
        return Response({
            "used": used,
            "limit": FREE_TIER_LIMIT,
            "remaining": max(FREE_TIER_LIMIT - used, 0),
        })