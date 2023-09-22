from django.conf.urls import url

from .views import WorkspaceAPIView, WorkspaceDetailAPIView, WorkspaceOutputView, WorkspacePromptListView

urlpatterns = [
    url(
        r"^api/v1/workspace/(?P<workspace_id>[0-9a-f-]+)/$",
        WorkspaceDetailAPIView.as_view(),
        name="workspace-info",
    ),
    url(r"^api/v1/workspace/create-workspace/$", WorkspaceAPIView.as_view(), name="workspace-create"),
    url(r"^api/v1/workspace/get-all-workspaces/$", WorkspaceAPIView.as_view(), name="workspace-list-all"),
    url(r"^api/v1/workspace/generate-output/$", WorkspaceOutputView.as_view(), name="workspace-output"),
    url(r"^api/v1/workspace/get-workspace-history/(?P<uuid>[0-9a-f-]+)/$", WorkspacePromptListView.as_view(), name="workspace-history"),
    url(
        r"^api/v1/workspace/search_workspace_history/$",
        WorkspaceDetailAPIView.as_view(),
        name="workspace-search",
    ),
    url(
        r"^api/v1/workspace/get-workspace-info/(?P<workspace_id>[0-9a-f-]+)/$",
        WorkspaceDetailAPIView.as_view(),
        name="workspace-info",
    ),
]
