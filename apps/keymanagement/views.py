import openai

from django.http import Http404
from rest_framework import status
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import KeyManagement, LLMProviders
from .serializers import KeyManagementSerializer

class KeyPageNumberPagination(PageNumberPagination):
    page_size = 5  # Adjust the page size as needed


class KeyManagementAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KeyManagementSerializer
    pagination_class = KeyPageNumberPagination  # Enable pagination for GET requests

    def get_queryset(self):
        return KeyManagement.objects.filter(user=self.request.user).order_by("-timestamp")

    # Override the create method to handle POST requests
    def create(self, request, *args, **kwargs):
        data = request.data
        data.update({"user": self.request.user.id})
        serializer = KeyManagementSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KeyManagementDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, uuid):
        try:
            return KeyManagement.objects.get(uuid=uuid, user=self.request.user)
        except KeyManagement.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        # Retrieve a key by UUID
        key = self.get_object(uuid)
        serializer = KeyManagementSerializer(key)
        return Response(serializer.data)

    def patch(self, request, uuid, format=None):
        # Update a key by UUID
        key = self.get_object(uuid)
        serializer = KeyManagementSerializer(key, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        # Delete a key by UUID
        key = self.get_object(uuid)
        key.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class KeyManagementProvidersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        provider_values = [provider.value for provider in LLMProviders]
        return Response(data=provider_values, status=status.HTTP_200_OK)

class TestKeyConnection(APIView):
   permission_classes = [IsAuthenticated]

   def post(self, request):
        api_key = request.data.get("api_key", "")
        provider = request.data.get("provider", "")
        if not api_key:
            return Response("key uuid is not valid", status=status.HTTP_400_BAD_REQUEST)

        if not provider:
            return Response("Please provide provider", status=status.HTTP_400_BAD_REQUEST)

        if provider ==  LLMProviders.OPENAI.value:
            try:
                openai.api_key = api_key
                openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt="this is test message",
                )
            except Exception as e:
                return Response("Invalid API key", status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response("Key is valid", status=status.HTTP_200_OK)
        else:
            return Response("This provider is not supported", status=status.HTTP_404_NOT_FOUND)