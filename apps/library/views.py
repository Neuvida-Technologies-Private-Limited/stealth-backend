# views.py
from rest_framework import generics
from .models import Prompt
from .serializers import PromptListSerializer
from rest_framework.pagination import PageNumberPagination  # Import the pagination class
from rest_framework.permissions import IsAuthenticated  # Import the IsAuthenticated permission

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
    queryset = Prompt.objects.filter(is_public=False)  # Filter prompts with is_public=True
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