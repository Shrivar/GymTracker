from django.contrib import admin
from django.urls import path, include
from django.views.defaults import permission_denied, server_error

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("tracker.urls")),
]

# Custom error handlers
handler403 = "django.views.defaults.permission_denied"
handler500 = "django.views.defaults.server_error"

