from django.http import Http404
from rest_framework import generics
from .models import Prompt
from .serializers import PromptListSerializer
from rest_framework.pagination import PageNumberPagination  # Import the pagination class
from rest_framework.permissions import IsAuthenticated  # Import the IsAuthenticated permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PublicPromptListView(generics.ListAPIView):
    queryset = Prompt.objects.filter(is_public=True)  # Filter prompts with is_public=True
    serializer_class = PromptListSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        # Include any context data you want to pass to the serializer
        context = super().get_serializer_context()
        # For example, you can include the current user
        context['user'] = self.request.user
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
        context['user'] = self.request.user
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
                return Response("is_public boolean value expected", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("uuid and is_public is expected", status=status.HTTP_400_BAD_REQUEST)
        prompt = Prompt.objects.filter(uuid=uuid, workspace__user=user, is_public=is_public).first()
        if not prompt:
            raise Http404
        if prompt.published:
            return Response("Prompt is already published", status=status.HTTP_400_BAD_REQUEST)

        prompt.published = True
        prompt.save()
        return Response("Prompt published successfully", status=status.HTTP_201_CREATED)