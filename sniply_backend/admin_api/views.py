from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .permissions import IsStaffOnly
from .serializers import AdminUserSerializer
from billing.models import Subscription, Plan

User = get_user_model()


class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsStaffOnly]
    queryset = User.objects.all().order_by("-date_joined")


class AdminUserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsStaffOnly]
    queryset = User.objects.all()


class AdminRevenueView(APIView):
    permission_classes = [IsStaffOnly]

    def get(self, request):
        total_users = User.objects.count()
        pro_subscriptions = Subscription.objects.filter(plan__name="Pro", status="active")
        pro_count = pro_subscriptions.count()

        pro_plan = Plan.objects.filter(name="Pro").first()
        mrr = float(pro_plan.price) * pro_count if pro_plan else 0

        thirty_days_ago = timezone.now() - timedelta(days=30)
        canceled_last_30 = Subscription.objects.filter(
            status="canceled"
        ).count()

        conversion_rate = (pro_count / total_users * 100) if total_users > 0 else 0

        return Response({
            "total_users": total_users,
            "pro_subscribers": pro_count,
            "mrr": mrr,
            "conversion_rate": round(conversion_rate, 2),
            "canceled_subscriptions": canceled_last_30,
        })


class AdminSubscriptionListView(generics.ListAPIView):
    permission_classes = [IsStaffOnly]
    queryset = Subscription.objects.select_related("user", "plan").order_by("-id")

    def list(self, request, *args, **kwargs):
        status_filter = request.query_params.get("status")
        qs = self.get_queryset()
        if status_filter:
            qs = qs.filter(status=status_filter)

        data = [
            {
                "user_email": sub.user.email,
                "plan": sub.plan.name,
                "status": sub.status,
                "current_period_end": sub.current_period_end,
            }
            for sub in qs
        ]
        return Response(data)