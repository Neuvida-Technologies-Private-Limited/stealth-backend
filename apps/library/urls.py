from django.conf.urls import url

from .views import (
    PublicPromptListView,
    PrivatePromptListView,
    PublishPromptView,
    PromptDetailView,
    PromptAddTagsView,
    LibraryPromptSearchView,
)

urlpatterns = [
    url(
        r"^api/v1/prompt/$",
        PromptDetailView.as_view(),
        name="prompt-info-public",
    ),
    url(
        r"^api/v1/prompt/get-prompt-list-public/$",
        PublicPromptListView.as_view(),
        name="prompt-list-public",
    ),
    url(
        r"^api/v1/prompt/search-prompt/$",
        LibraryPromptSearchView.as_view(),
        name="prompt-search-library",
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
    url(
        r"^api/v1/prompt/(?P<prompt_uuid>[0-9a-f-]+)/$",
        PromptDetailView.as_view(),
        name="prompt-info-public",
    ),
    url(
        r"^api/v1/prompt/(?P<prompt_uuid>[0-9a-f-]+)/add-tags/$",
        PromptAddTagsView.as_view(),
        name="prompt-info-public",
    ),
]
