import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Plan, Subscription
from .services import create_checkout_session

User = get_user_model()


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            pro_plan = Plan.objects.get(name="Pro")
        except Plan.DoesNotExist:
            return Response({"detail": "Pro plan not configured"}, status=400)

        session = create_checkout_session(
            user=request.user,
            plan=pro_plan,
            success_url="https://sniply-frontend-five.vercel.app/billing/success",
            cancel_url="https://sniply-frontend-five.vercel.app/billing/cancel",
        )
        return Response({"checkout_url": session.url})


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return HttpResponse(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            self._handle_checkout_completed(session)

        elif event["type"] == "customer.subscription.deleted":
            subscription_obj = event["data"]["object"]
            self._handle_subscription_deleted(subscription_obj)

        return HttpResponse(status=200)

    def _handle_checkout_completed(self, session):
        customer_id = session.customer
        stripe_subscription_id = session.subscription

        try:
            user = User.objects.get(stripe_customer_id=customer_id)
        except User.DoesNotExist:
            return

        pro_plan = Plan.objects.get(name="Pro")

        Subscription.objects.update_or_create(
            user=user,
            defaults={
                "plan": pro_plan,
                "status": "active",
                "stripe_subscription_id": stripe_subscription_id,
            },
        )

    def _handle_subscription_deleted(self, subscription_obj):
        stripe_subscription_id = subscription_obj.id
        try:
            subscription = Subscription.objects.get(stripe_subscription_id=stripe_subscription_id)
        except Subscription.DoesNotExist:
            return

        free_plan = Plan.objects.get(name="Free")
        subscription.plan = free_plan
        subscription.status = "canceled"
        subscription.save()