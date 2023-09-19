from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r"^api/v1/access/login/$", views.login_view, name="login-view"),
    url(r"^api/v1/access/signup/$", views.SignupAPIView.as_view(), name="signup-view"),
    url(
        r"^api/v1/access/refresh/$",
        views.custom_token_refresh_view,
        name="custom-token-refresh",
    ),
    url(
        r"^api/v1/access/verify-email/(?P<uuid>[0-9a-f-]+)/(?P<token>[0-9a-f-]+)/$",
        views.VerifyEmailView.as_view(),
        name="verify-email-view",
    ),
    url(
        r"^api/v1/access/current-user/$",
        views.CurrentUserAPIView.as_view(),
        name="current-user",
    ),
    url(r"^api/v1/access/", include("allauth.urls")),
]
