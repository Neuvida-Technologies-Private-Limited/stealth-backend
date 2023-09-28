from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uuid", "email", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.filter(
            email=validated_data["email"]
        )
        if user:
            raise serializers.ValidationError(
                {"error": "User already exists with this email ID"}
            )
        user = User.objects.create(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.first_name = validated_data.get("first_name", "")
        user.last_name = validated_data.get("last_name", "")
        user.save()
        return user
