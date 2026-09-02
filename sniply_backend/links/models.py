import random
import string
from django.conf import settings
from django.db import models


def generate_short_code(length=7):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))


class Link(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="links")
    short_code = models.CharField(max_length=20, unique=True)
    original_url = models.URLField(max_length=2000)
    custom_domain = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            code = generate_short_code()
            while Link.objects.filter(short_code=code).exists():
                code = generate_short_code()
            self.short_code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"