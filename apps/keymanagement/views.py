from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import KeyManagement
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
            return KeyManagement.objects.get(uuid=uuid)
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
