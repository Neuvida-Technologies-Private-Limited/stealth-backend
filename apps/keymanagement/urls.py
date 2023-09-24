from django.conf.urls import url

from .views import (
    KeyManagementAPIView,
    KeyManagementDetailAPIView,
    KeyManagementProvidersView,
)

urlpatterns = [
    url(
        r"^api/v1/key/get_key_list/$",
        KeyManagementAPIView.as_view(),
        name="keymanagement-list",
    ),
    url(
        r"^api/v1/key/create_key/$",
        KeyManagementAPIView.as_view(),
        name="keymanagement-create",
    ),
    url(
        r"^api/v1/key/llm-providers/$",
        KeyManagementProvidersView.as_view(),
        name="keymanagement-create",
    ),
    url(
        r"^api/v1/key/(?P<uuid>[0-9a-f-]+)/$",
        KeyManagementDetailAPIView.as_view(),
        name="keymanagement-detail",
    ),
]
