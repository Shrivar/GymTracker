from django.conf import settings
from django.shortcuts import render


EXEMPT_PATHS = (
    "/accounts/",
    "/admin/",
    "/static/",
)


class AuthorizedUserMiddleware:
    """
    Restricts the application to a single authorized email address.
    Unauthenticated users are passed through (allauth handles the login flow).
    Authenticated users whose email doesn't match AUTHORIZED_EMAIL see a 403 page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Let allauth/admin/static paths through unconditionally
        if any(request.path.startswith(p) for p in EXEMPT_PATHS):
            return self.get_response(request)

        # Unauthenticated users — let Django/allauth redirect to login as normal
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Authenticated but not the authorized user
        authorized_email = getattr(settings, "AUTHORIZED_EMAIL", "")
        if authorized_email and request.user.email != authorized_email:
            return render(request, "403.html", status=403)

        return self.get_response(request)

