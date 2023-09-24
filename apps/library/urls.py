from django.conf.urls import url

from .views import PublicPromptListView, PrivatePromptListView, PublishPromptView

urlpatterns = [
    url(
        r"^api/v1/prompt/get-prompt-list-public/$",
        PublicPromptListView.as_view(),
        name="prompt-list-public",
    ),
    url(
        r"^api/v1/prompt/get-prompt-list-private/$",
        PrivatePromptListView.as_view(),
        name="prompt-list-private",
    ),
    url(
        r"^api/v1/prompt/publish-prompt/$",
        PublishPromptView.as_view(),
        name="prompt-publish",
    ),
]
