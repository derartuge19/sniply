from django.urls import path
from .views import LinkListCreateView, LinkDetailView, LinkQRCodeView

urlpatterns = [
    path("", LinkListCreateView.as_view(), name="link-list-create"),
    path("<int:pk>/", LinkDetailView.as_view(), name="link-detail"),
     path("<int:pk>/qr/", LinkQRCodeView.as_view(), name="link-qr"),
]