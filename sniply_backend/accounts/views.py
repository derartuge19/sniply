from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        from billing.models import Plan, Subscription
        free_plan = Plan.objects.get(name="Free")
        Subscription.objects.create(user=user, plan=free_plan, status="active")

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {"id": user.id, "email": user.email, "username": user.username},
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {"id": user.id, "email": user.email, "username": user.username, "is_staff": user.is_staff},
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


class GoogleAuthView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(
                token, google_requests.Request(), settings.GOOGLE_CLIENT_ID
            )
        except ValueError:
            return Response({"detail": "Invalid Google token"}, status=status.HTTP_401_UNAUTHORIZED)

        google_id = idinfo["sub"]
        email = idinfo["email"]
        name = idinfo.get("name", email.split("@")[0])

        user, created = User.objects.get_or_create(
            google_id=google_id,
            defaults={
                "email": email,
                "username": name,
                "auth_provider": "google",
            },
        )

        if created:
            from billing.models import Plan, Subscription
            free_plan = Plan.objects.get(name="Free")
            Subscription.objects.create(user=user, plan=free_plan, status="active")

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {"id": user.id, "email": user.email, "username": user.username, "is_staff": user.is_staff},
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })