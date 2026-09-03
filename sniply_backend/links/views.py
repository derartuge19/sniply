import qrcode
import io
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from .models import Link
from .serializers import LinkSerializer
from tracking.models import Click
from core.utils import hash_ip, get_client_ip
from usage.permissions import HasLinkQuotaRemaining, IsProUser
from usage.services import increment_usage


class LinkListCreateView(generics.ListCreateAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated, HasLinkQuotaRemaining]

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        increment_usage(self.request.user)


class LinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        try:
            is_pro = self.request.user.subscription.plan.name == "Pro"
        except AttributeError:
            is_pro = False

        if not is_pro and "original_url" in self.request.data:
            raise PermissionDenied("Editing a link's destination is a Pro feature. Upgrade to use this.")

        serializer.save()


class LinkQRCodeView(APIView):
    permission_classes = [IsAuthenticated, IsProUser]

    def get(self, request, pk):
        link = get_object_or_404(Link, pk=pk, user=request.user)
        short_url = request.build_absolute_uri(f"/{link.short_code}")

        qr = qrcode.make(short_url)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type="image/png")


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