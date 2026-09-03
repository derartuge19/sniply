from django.db import models
from django.conf import settings


class UsageCounter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="usage_counters")
    period_start = models.DateField()
    period_end = models.DateField()
    links_created_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "period_start")

    def __str__(self):
        return f"{self.user.email}: {self.links_created_count} links ({self.period_start} to {self.period_end})"