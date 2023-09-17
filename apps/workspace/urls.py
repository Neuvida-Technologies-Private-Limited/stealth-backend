from django.conf.urls import url

from .views import WorkspaceAPIView, WorkspaceDetailAPIView

urlpatterns = [
    url(r"^api/v1/workspace/$", WorkspaceAPIView.as_view(), name='workspace-list'),
    url(r"^api/v1/workspace/search_workspace_history/$", WorkspaceDetailAPIView.as_view(), name='workspace-search'),
    url(r"^api/v1/workspace/(?P<workspace_id>[0-9a-f-]+)/$", WorkspaceDetailAPIView.as_view(), name='workspace-detail'),
]