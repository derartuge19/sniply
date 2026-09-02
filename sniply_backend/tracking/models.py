from django.db import models
from links.models import Link


class Click(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="clicks")
    clicked_at = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=500, blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    ip_hash = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Click on {self.link.short_code} at {self.clicked_at}"