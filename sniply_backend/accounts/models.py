from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    AUTH_PROVIDER_CHOICES = (
        
        ("email","Email"),
        ("google" , "Google"),
    )
    
    email = models.EmailField(unique=True)
    auth_provider = models.CharField(
        max_length=10, choices=AUTH_PROVIDER_CHOICES, default="email"
    )
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    
    def __str__(self):
        return self.email

# Create your models here.
