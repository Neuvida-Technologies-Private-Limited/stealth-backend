from django.conf.urls import url

from .views import PublicPromptListView, PrivatePromptListView

urlpatterns = [
    url(
        r"^api/v1/prompt/get-prompt-list-public/$",
        PublicPromptListView.as_view(),
        name="prompt-list",
    ),
    url(
        r"^api/v1/prompt/get-prompt-list-private/$",
        PrivatePromptListView.as_view(),
        name="prompt-list",
    ),
]
