from django.urls import path
from .views import RegisterView, LoginView, GoogleAuthView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("google/", GoogleAuthView.as_view(), name="google_auth"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]