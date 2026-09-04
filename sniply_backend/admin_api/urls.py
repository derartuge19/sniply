from django.urls import path
from .views import AdminUserListView, AdminUserDetailView, AdminRevenueView, AdminSubscriptionListView

urlpatterns = [
    path("users/", AdminUserListView.as_view(), name="admin-users"),
    path("users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"),
    path("revenue/", AdminRevenueView.as_view(), name="admin-revenue"),
    path("subscriptions/", AdminSubscriptionListView.as_view(), name="admin-subscriptions"),
]