from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "username")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            email=validated_data["email"],
        )
        if not created:
            raise serializers.ValidationError(
                {"error": "User already exists with this email ID"}
            )
        user.username = validated_data["username"]
        user.set_password(validated_data["password"])
        user.save()
        return user
