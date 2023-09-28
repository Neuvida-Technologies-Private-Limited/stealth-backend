from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Exclude the 'user' field from the serialized data
        data.pop("user")
        data.update({"user_uuid": instance.user.uuid})
        data.update({"first_name": instance.user.first_name})
        data.update({"last_name": instance.user.last_name})
        return data

    class Meta:
        model = Workspace
        fields = [
            "id",
            "title",
            "model_key",
            "user",
            "last_modified",
            "timestamp",
        ]  # List the fields you want to include
