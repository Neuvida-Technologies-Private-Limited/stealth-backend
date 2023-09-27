import openai

from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import KeyManagement, LLMProviders
from .serializers import KeyManagementSerializer


class KeyManagementAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get all keys
        keys = KeyManagement.objects.filter(user=request.user)
        serializer = KeyManagementSerializer(keys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Create a new key
        data = request.data
        data.update({"user": request.user.id})
        serializer = KeyManagementSerializer(data=request.data)
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