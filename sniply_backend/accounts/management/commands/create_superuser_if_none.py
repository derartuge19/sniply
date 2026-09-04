from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a superuser from environment variables if one doesn't already exist"

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")

        if not email or not password:
            self.stdout.write("Skipping superuser creation: env vars not set")
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write("Superuser already exists, skipping")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser {email} created"))