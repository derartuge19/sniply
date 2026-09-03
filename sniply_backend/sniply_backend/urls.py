from django.contrib import admin
from django.urls import path, include
from links.views import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/links/", include("links.urls")),
    path("<str:short_code>/", RedirectView.as_view(), name="redirect"),
    path("api/usage/", include("usage.urls")),
]