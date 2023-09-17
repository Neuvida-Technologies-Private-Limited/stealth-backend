from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Workspace

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'title', 'model_key', 'user']  # List the fields you want to include
