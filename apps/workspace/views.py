from django.db.models import Q
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django.db import transaction
from apps.library.services import LLMServiceFactory
from .models import Workspace
from .serializers import WorkspaceSerializer
from apps.library.serializers import (
    GenerateOutputSerializer,
    PromptHistoryListSerializer,
)
from apps.library.models import Model, Parameter, ParameterMapping, Prompt

class CustomWorkspacePagination(PageNumberPagination):
    page_size = 10  # Set your custom page size here


class WorkspaceAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkspaceSerializer
    pagination_class = CustomWorkspacePagination  # Enable pagination for GET requests

    def get_queryset(self):
        # Customize the queryset as needed
        return Workspace.objects.filter(user=self.request.user).order_by("-timestamp")

    # Override the create method to handle POST requests
    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({"user": request.user.id})
        serializer = WorkspaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
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
        workspace_uuid = data.get("workspace", "")
        tags = data.pop("tags", "")
        try:
            workspace = Workspace.objects.get(id=workspace_uuid, user=self.request.user)
            if not workspace.model_key:
                return Response(
                    {"message": "Workspace key not found."}, status=status.HTTP_404_NOT_FOUND
                )
        except Workspace.DoesNotExist:
            return Response(
                {"message": "Workspace not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = GenerateOutputSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data["workspace"] = workspace
            try:
                prompt = serializer.save()
                if tags:
                    prompt.tags = tags
                    prompt.save()
                for param, value in parameters.items():
                    llm_model, _ = Model.objects.get_or_create(
                        name=prompt.workspace.model_key.provider
                    )
                    parameter, _ = Parameter.objects.get_or_create(name=param)
                    ParameterMapping.objects.create(
                        prompt=prompt, model=llm_model, parameter=parameter, value=value
                    )
                provider = LLMServiceFactory.create_llm_service(prompt)
                # Call the OpenAIProvider service here
                provider.run()
                serializer = PromptHistoryListSerializer(prompt)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                # Handle exceptions raised by the service
                # Rollback the database transaction
                print("Exception is", e)
                transaction.set_rollback(True)
                return Response(
                    {"message": "Error generating prompt"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspacePromptListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        # Retrieve all prompts associated with the given workspace
        published = self.request.query_params.get("published", "False")
        if published not in ["True", "False"]:
            return Response(
                "Invalid choice valid choices are True, False",
                status=status.HTTP_400_BAD_REQUEST,
            )
        prompts = Prompt.objects.filter(
            workspace_id=uuid,
            workspace__user=self.request.user,
            is_public=False,
            published=published,
        ).order_by("timestamp")
        serializer = PromptHistoryListSerializer(prompts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed


class WorkspacePromptSearchView(generics.ListAPIView):
    serializer_class = PromptHistoryListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination  # Use your custom pagination class here
    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        query = self.request.query_params.get("q", "")
        queryset = Prompt.objects.filter(
            workspace=workspace_id, workspace__user=self.request.user
        )
        if not queryset:
            raise Http404
        search_result = []
        if query:
            # Split the search query into individual words
            search_terms = query.split()

            # Create a Q object to combine multiple conditions using OR
            q_objects = Q()
            prompt_tags = []
            for prompt in queryset:
                if prompt.tag_exists(query):
                    prompt_tags.append(prompt)
            # Search in title, system message, user message, and PromptOutput
            for term in search_terms:
                q_objects |= (
                    Q(title__icontains=term)
                    | Q(system_message__icontains=term)
                    | Q(user_message__icontains=term)
                    | Q(
                        prompt_output__output__icontains=term
                    )  # Search in PromptOutput table
                )

            # Search for tags that contain the search term

            # Apply the combined Q object to filter the queryset
            queryset = queryset.filter(q_objects)
            for prompt in prompt_tags:
                if not queryset.filter(id=prompt.id):
                    search_result.append(prompt)
            search_result = search_result + list(queryset)
        return search_result
