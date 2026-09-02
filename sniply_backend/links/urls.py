from django.urls import path
from .views import LinkListCreateView, LinkDetailView

urlpatterns = [
    path("", LinkListCreateView.as_view(), name="link-list-create"),
    path("<int:pk>/", LinkDetailView.as_view(), name="link-detail"),
]