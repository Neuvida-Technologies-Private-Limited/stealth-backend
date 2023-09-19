from django.contrib.auth.models import User
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Workspace
from .serializers import WorkspaceSerializer


class WorkspaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve all workspaces
        workspaces = Workspace.objects.filter(user=request.user)
        serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new workspace
        data = request.data
        data.update({"user": request.user.id})
        serializer = WorkspaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspaceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, workspace_id):
        try:
            return Workspace.objects.get(pk=workspace_id)
        except Workspace.DoesNotExist:
            raise Http404

    def get(self, request, workspace_id):
        # Retrieve a single workspace by its id
        workspace = self.get_object(workspace_id)
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data)

    def patch(self, request, workspace_id):
        # Update an existing workspace by its id
        workspace = self.get_object(workspace_id)
        serializer = WorkspaceSerializer(workspace, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, workspace_id):
        # Delete an existing workspace by its id
        workspace = self.get_object(workspace_id)
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkspaceOutputView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass

class SearchWorkspaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass
