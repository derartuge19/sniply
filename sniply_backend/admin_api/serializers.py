from rest_framework import serializers
from django.contrib.auth import get_user_model
from billing.models import Subscription

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField()
    subscription_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "date_joined", "is_staff", "plan_name", "subscription_status"]

    def get_plan_name(self, obj):
        try:
            return obj.subscription.plan.name
        except AttributeError:
            return None

    def get_subscription_status(self, obj):
        try:
            return obj.subscription.status
        except AttributeError:
            return None