from django.db import models
from django.conf import settings


class Plan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    link_limit = models.IntegerField(null=True, blank=True)
    custom_domain_allowed = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("past_due", "Past Due"),
        ("canceled", "Canceled"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    current_period_end = models.DateTimeField(null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"