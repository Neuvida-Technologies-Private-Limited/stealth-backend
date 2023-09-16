from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Workspace

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'title', 'model_key']  # List the fields you want to include

    def create(self, validated_data):
        # Get the currently authenticated user from the serializer's context
        user: User = self.context.get("user")

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")

        # Create a new Workspace instance and set the user
        workspace = Workspace.objects.create(user=user, **validated_data)

        return workspace