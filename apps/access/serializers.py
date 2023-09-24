from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uuid", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            email=validated_data["email"],
        )
        if not created:
            raise serializers.ValidationError(
                {"error": "User already exists with this email ID"}
            )
        user.set_password(validated_data["password"])
        user.save()
        return user
