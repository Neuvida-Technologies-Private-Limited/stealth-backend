from rest_framework import serializers, generics
from .models import KeyManagement


class KeyManagementSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Exclude the 'user' field from the serialized data
        data.pop('user')
        data.update({"user_uuid": instance.user.uuid})
        return data

    class Meta:
        model = KeyManagement
        fields = ("uuid", "title", "user", "api_key", "description")
