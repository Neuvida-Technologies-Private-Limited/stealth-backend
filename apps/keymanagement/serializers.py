from rest_framework import serializers, generics
from .models import KeyManagement


class KeyManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyManagement
        fields = ("uuid", "title", "user", "api_key")
