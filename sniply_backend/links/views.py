from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from .models import Link
from .serializers import LinkSerializer
from tracking.models import Click
from core.utils import hash_ip, get_client_ip


class LinkListCreateView(generics.ListCreateAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class RedirectView(View):
    def get(self, request, short_code):
        link = get_object_or_404(Link, short_code=short_code, is_active=True)

        Click.objects.create(
            link=link,
            referrer=request.META.get("HTTP_REFERER", ""),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            ip_hash=hash_ip(get_client_ip(request)),
        )

        return redirect(link.original_url)