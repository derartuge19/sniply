from django.urls import path
from .views import LinkAnalyticsView

urlpatterns = [
    path("<int:pk>/", LinkAnalyticsView.as_view(), name="link-analytics"),
]