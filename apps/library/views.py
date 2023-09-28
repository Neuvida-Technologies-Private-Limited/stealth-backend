from django.http import Http404
from rest_framework import generics
from .models import Prompt
from .serializers import PromptListSerializer, PromptSerializer
from rest_framework.pagination import (
    PageNumberPagination,
)  # Import the pagination class
from rest_framework.permissions import (
    IsAuthenticated,
)  # Import the IsAuthenticated permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tagging.models import Tag


class PublicPromptListView(generics.ListAPIView):
    queryset = Prompt.objects.filter(
        is_public=True
    )  # Filter prompts with is_public=True
    serializer_class = PromptListSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        # Include any context data you want to pass to the serializer
        context = super().get_serializer_context()
        # For example, you can include the current user
        context["user"] = self.request.user
        return context


class PrivatePromptListView(generics.ListAPIView):
    serializer_class = PromptListSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter prompts with is_public=False for the current user
        return Prompt.objects.filter(is_public=False, workspace__user=self.request.user)

    def get_serializer_context(self):
        # Include any context data you want to pass to the serializer
        context = super().get_serializer_context()
        # For example, you can include the current user
        context["user"] = self.request.user
        return context


class PublishPromptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        try:
            uuid = data["uuid"]
            is_public = data["is_public"]
            if type(is_public) != bool:
                return Response(
                    "is_public boolean value expected",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                "uuid and is_public is expected", status=status.HTTP_400_BAD_REQUEST
            )
        prompt = Prompt.objects.filter(
            uuid=uuid, workspace__user=user, is_public=is_public
        ).first()
        if not prompt:
            raise Http404
        if prompt.published:
            return Response(
                "Prompt is already published", status=status.HTTP_400_BAD_REQUEST
            )

        prompt.published = True
        prompt.save()
        return Response("Prompt published successfully", status=status.HTTP_201_CREATED)

class PromptDetailView(APIView):
    def get(self, request, prompt_uuid):
        try:
            prompt = Prompt.objects.get(uuid=prompt_uuid)
            serializer = PromptSerializer(prompt, context = {"user": request.user})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Prompt.DoesNotExist:
            return Response({'message': 'Prompt not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, prompt_uuid):
        try:
            prompt = Prompt.objects.get(uuid=prompt_uuid)
            print(6454)
            serializer = PromptSerializer(prompt,context = {"user": request.user}, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Prompt.DoesNotExist:
            return Response({'message': 'Prompt not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, prompt_uuid):
        try:
            prompt = Prompt.objects.get(uuid=prompt_uuid)
            prompt.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Prompt.DoesNotExist:
            return Response({'message': 'Prompt not found'}, status=status.HTTP_404_NOT_FOUND)

class PromptAddTagsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, prompt_uuid):
        try:
            prompt = Prompt.objects.get(uuid=prompt_uuid)
        except:
            raise Http404
        tag_data = request.data.get("tags", [])
        tags = Tag.objects.get_for_object(prompt)
        tags_set = set()
        for tag in tags:
            tags_set.add(tag.name)

        for tag in tag_data:
            if tag not in tags_set:
                Tag.objects.add_tag(prompt, tag)

        return Response("Tags added", status=status.HTTP_201_CREATED)