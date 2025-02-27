from .models import Prompt, LikeDislikePrompt, PromptOutput, PromptVariable
from rest_framework import serializers


class GenerateOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = [
            "user",
            "workspace",
            "title",
            "system_message",
            "user_message",
            "is_public",
            "bookmarked",
            "prompt_type",
        ]  # You can specify the fields you want to include explicitly if needed


class PromptOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptOutput
        fields = ["output"]

class PromptVariablesSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = PromptVariable
        fields = ["key", "value"]


class PromptHistoryListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    prompt_output = PromptOutputSerializer(many=True)
    variables = PromptVariablesSeriaizer(many=True)
    class Meta:
        model = Prompt
        fields = [
            "title",
            "is_public",
            "bookmarked",
            "prompt_type",
            "sample_output",
            "tags",
            "system_message",
            "user_message",
            "prompt_output",
            "uuid",
            "published",
            "variables"
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        prompt_output = data.pop("prompt_output")
        data["prompt_output"] = [output_dict["output"] for output_dict in prompt_output]
        variables = data.pop("variables", [])
        variables_dict = {item["key"]: item["value"] for item in variables}
        data["variables"] = variables_dict
        return data

    def get_tags(self, obj):
        return list(obj.tags.all().values_list("name", flat=True))


class PromptListSerializer(serializers.ModelSerializer):
    likes_dislikes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    variables = PromptVariablesSeriaizer(many=True)

    class Meta:
        model = Prompt
        fields = (
            "title",
            "published",
            "is_public",
            "bookmarked",
            "prompt_type",
            "user_message",
            "sample_output",
            "likes_dislikes_count",
            "liked_by_user",
            "tags",
            "uuid",
            "favourite",
            "system_message",
            "variables",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        variables = data.pop("variables", [])
        variables_dict = {item["key"]: item["value"] for item in variables}
        data["variables"] = variables_dict
        return data

    def get_tags(self, obj):
        return list(obj.tags.all().values_list("name", flat=True))

    def get_likes_dislikes_count(self, obj):
        likes_count = obj.likes_dislikes.filter(liked=True).count()
        dislikes_count = obj.likes_dislikes.filter(liked=False).count()
        return {"likes": likes_count, "dislikes": dislikes_count}

    def get_liked_by_user(self, obj):
        user = self.context["user"]  # Retrieve user from context
        prompt = obj  # The current prompt instance

        try:
            like_dislike = LikeDislikePrompt.objects.get(prompt=prompt, user=user)
            return like_dislike.liked
        except LikeDislikePrompt.DoesNotExist:
            return None  # If there's no like/dislike record


class PromptSerializer(serializers.ModelSerializer):
    likes_dislikes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    prompt_type = serializers.CharField(required=False)
    user_message = serializers.CharField(max_length=1000)
    system_message = serializers.CharField(max_length=1000)
    sample_output = serializers.CharField(max_length=1000)
    title = serializers.CharField(max_length=100)
    bookmarked = serializers.BooleanField(required=False)
    variables = PromptVariablesSeriaizer(many=True, required=False)

    def get_tags(self, obj):
        return list(obj.tags.all().values_list("name", flat=True))

    def get_likes_dislikes_count(self, obj):
        likes_count = obj.likes_dislikes.filter(liked=True).count()
        dislikes_count = obj.likes_dislikes.filter(liked=False).count()
        return {"likes": likes_count, "dislikes": dislikes_count}

    def get_liked_by_user(self, obj):
        user = self.context["user"]  # Retrieve user from context
        prompt = obj  # The current prompt instance

        try:
            like_dislike = LikeDislikePrompt.objects.get(prompt=prompt, user=user)
            return like_dislike.liked
        except LikeDislikePrompt.DoesNotExist:
            return None  # If there's no like/dislike record

    def to_representation(self, instance):
        data = super().to_representation(instance)
        variables = data.pop("variables", [])
        variables_dict = {item["key"]: item["value"] for item in variables}
        data["variables"] = variables_dict
        return data

    def create(self, validated_data):
        tags =  self.context["tags"]
        user = self.context["user"]
        tags_list = tags.split(",")
        if len(tags_list) > 5:
            raise serializers.ValidationError({"tags": "Max 5 tags allowed"})
        for tag in tags_list:
            if len(tag) > 100:
                raise serializers.ValidationError({"tags": "Tag max length can be 100 characters"})
        prompt = super().create(validated_data)
        prompt.tags = tags
        prompt.user = user
        prompt.save()
        return prompt

    def update(self, instance, validated_data):
        liked = self.context.get("liked", None)
        user = self.context["user"]
        if liked == "delete":
            LikeDislikePrompt.objects.filter(prompt=instance, user=user).delete()
        elif liked != None:
            liked_obj, _ = LikeDislikePrompt.objects.get_or_create(prompt=instance, user=user)
            liked_obj.liked = liked
            liked_obj.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Prompt
        fields = [
            "title",
            "system_message",
            "user_message",
            "sample_output",
            "favourite",
            "published",
            "is_public",
            "prompt_type",
            "workspace",
            "likes_dislikes_count",
            "liked_by_user",
            "tags",
            "bookmarked",
            "variables",
        ]
