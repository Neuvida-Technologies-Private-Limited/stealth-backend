from .models import Prompt, LikeDislikePrompt, PromptOutput
from rest_framework import serializers


class GenerateOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ["workspace", "title", "system_message", "user_message", "is_public", "bookmarked", "prompt_type"]  # You can specify the fields you want to include explicitly if needed

class PromptOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptOutput
        fields = ["output"]

class PromptHistoryListSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    prompt_output = PromptOutputSerializer(many=True)
    class Meta:
        model = Prompt
        fields = ["title", "is_public", "bookmarked", "prompt_type", "sample_output", "tags", "system_message", "user_message", "prompt_output", "uuid"]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        prompt_output = data.pop("prompt_output")
        data["prompt_output"] = [output_dict["output"] for output_dict in prompt_output]
        return data

    def get_tags(self, obj):
        return list(obj.tags.all().values_list("name", flat=True))

class PromptListSerializer(serializers.ModelSerializer):
    likes_dislikes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Prompt
        fields = ("title", "is_public", "bookmarked", "prompt_type", "user_message", "sample_output", "likes_dislikes_count", "liked_by_user", "tags", "uuid")

    def get_tags(self, obj):
        return list(obj.tags.all().values_list("name", flat=True))

    def get_likes_dislikes_count(self, obj):
        likes_count = obj.likes_dislikes.filter(liked=True).count()
        dislikes_count = obj.likes_dislikes.filter(liked=False).count()
        return {'likes': likes_count, 'dislikes': dislikes_count}

    def get_liked_by_user(self, obj):
        user = self.context['user']  # Retrieve user from context
        prompt = obj  # The current prompt instance

        try:
            like_dislike = LikeDislikePrompt.objects.get(prompt=prompt, user=user)
            return like_dislike.liked
        except LikeDislikePrompt.DoesNotExist:
            return None  # If there's no like/dislike record
