from django.contrib.auth.models import User
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from apps.library.services import LLMServiceFactory
from .models import Workspace
from .serializers import WorkspaceSerializer
from apps.library.serializers import GenerateOutputSerializer, PromptHistoryListSerializer
from apps.library.models import Model, Parameter, ParameterMapping, Prompt
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
            return Workspace.objects.get(pk=workspace_id, user=self.request.user)
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

    @transaction.atomic
    def post(self, request):
        data = request.data
        parameters = data.pop("parameters", {})
        workspace_uuid = data.get('workspace', '')
        
        try:
            workspace = Workspace.objects.get(id=workspace_uuid)
        except Workspace.DoesNotExist:
            return Response({"message": "Workspace not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = GenerateOutputSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['workspace'] = workspace
            try:
                prompt = serializer.save()
                for param, value in parameters.items():
                    llm_model, _ = Model.objects.get_or_create(name=prompt.workspace.model_key.provider)
                    parameter, _ = Parameter.objects.get_or_create(name=param)
                    ParameterMapping.objects.create(prompt=prompt, model=llm_model, parameter=parameter, value=value)
                provider = LLMServiceFactory.create_llm_service(prompt)
                # Call the OpenAIProvider service here
                provider.run()
                return Response({"message": prompt.prompt_output.last().output}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Handle exceptions raised by the service
                # Rollback the database transaction
                print("Exception is", e)
                transaction.set_rollback(True)
                return Response({"message": "Error generating prompt"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchWorkspaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass

class WorkspacePromptListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        # Retrieve all prompts associated with the given workspace
        prompts = Prompt.objects.filter(workspace_id=uuid, workspace__user=self.request.user).order_by("timestamp")
        serializer = PromptHistoryListSerializer(prompts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)