from django.conf.urls import url

from .api import WorkspaceAPIView, WorkspaceDetailAPIView

urlpatterns = [
    url(r"^api/v1/workspace/$", WorkspaceAPIView.as_view(), name='workspace-list'),
    url(r"^api/v1/workspace/(?P<workspace_id>\d+)/$", WorkspaceDetailAPIView.as_view(), name='workspace-detail'),
]