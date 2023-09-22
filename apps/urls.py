from django.urls import include, path

urlpatterns = [
    path("", include("apps.core.urls")),  # entry point to other project app urls
    path("", include("apps.workspace.urls")),
    path("", include("apps.access.urls")),
    path("", include("apps.keymanagement.urls")),
    path("", include("apps.library.urls")),
]
