from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from links.models import Link
from .services import get_link_analytics


class LinkAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk, user=request.user)
        days = int(request.query_params.get("days", 30))
        data = get_link_analytics(link, days=days)
        return Response(data)