import uuid
from enum import Enum

from django.db import models
from django.db.models import UniqueConstraint
from tagging.registry import register

from apps.access.models import User
from apps.core.models import Base, Ownable
from apps.workspace.models import Workspace
from apps.keymanagement.models import LLMProviders


class ParameterEnum(Enum):
    TEMPERATURE = "temperature"
    MAXIMUM_LENGTH = "maximum_length"
    STOP_SEQUENCE = "stop_sequence"
    TOP_P = "top_p"
    FREQUENCY_PENALTY = "frequency_penalty"
    PRESENCE_PENALTY = "presence_penalty"
    LOGIT_BIAS = "logit_bias"


class Parameter(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(
        max_length=255,
        choices=[(choice.value, choice.name) for choice in ParameterEnum],
        unique=True,
    )
    description = models.TextField()  # Description of the parameter

    def __str__(self):
        return self.name


class Model(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(
        max_length=255,
        choices=[(choice.value, choice.name) for choice in LLMProviders],
        unique=True,
    )

    def __str__(self):
        return self.name


class PromptTypeEnum(Enum):
    CHAT = "Chat"
    COMPLETION = "Completion"


class Prompt(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)  # Title of the prompt
    system_message = models.TextField()  # System-generated message
    user_message = models.TextField()  # User input message
    sample_output = models.TextField()  # Output generated by the prompt
    bookmarked = models.BooleanField(default=False)  # Is the prompt bookmarked
    published = models.BooleanField(default=False)  # Is the prompt saved
    is_public = models.BooleanField(default=False)
    prompt_type = models.CharField(
        max_length=255,
        choices=[(choice.value, choice.name) for choice in PromptTypeEnum],
    )
    # if a prompt is published then it will belong to a user instead of workspace
    # so event if workspace is deleted it will be there in user's library using this relation
    user = models.ForeignKey(User, blank=True, null=True, related_name="prompts", on_delete=models.CASCADE)
    workspace = models.ForeignKey(
        Workspace,  # ForeignKey to associate with a Workspace
        on_delete=models.SET_NULL,  # Set workspace to NULL when deleted
        related_name="prompts",  # For accessing prompts in a workspace
        blank=True,  # Allows for null values, indicating that it's not associated with a workspace
        null=True,
    )
    favourite = models.BooleanField(default=False)

    def tag_exists(self, value):
        all_tags = self.tags.values_list("name", flat=True)
        for tag in all_tags:
            if value.lower() in tag.lower():
                return True
        return False

    def copy_published_prompt(self, user, is_public=False):
            """
            Create a copy of the current prompt with the specified user and other attributes.
            """
            copied_prompt = Prompt.objects.create(
                title=self.title,
                system_message=self.system_message,
                user_message=self.user_message,
                sample_output=self.sample_output,
                bookmarked=self.bookmarked,
                published=True,  # Set as published
                is_public=is_public,  # Set as not public
                prompt_type=self.prompt_type,
                user=user,  # Set the user to the provided user
                workspace=None,  # Set workspace to None
                favourite=self.favourite,
            )
            
            # copy variables
            variables = self.variables.all()
            for variable in variables:
                PromptVariable.objects.create(
                    prompt = copied_prompt,
                    value = variable.value,
                    key = variable.key
                )


            # Copy tags (if you have a many-to-many relationship)
            copied_prompt.tags = ",".join(self.tags.all().values_list("name", flat=True))

            copied_prompt.save()

            return copied_prompt

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.workspace:
            self.workspace.save()
        return super().save(*args, **kwargs)

# this will tags to prompts
register(Prompt)


# Create your models here.
class LikeDislikePrompt(Base, Ownable):
    prompt = models.ForeignKey(
        Prompt, on_delete=models.CASCADE, related_name="likes_dislikes"
    )  # Related prompt
    liked = models.BooleanField(default=True)  # True for like, False for dislike

    def __str__(self):
        status = "Liked" if self.liked else "Disliked"
        return f"{status}: {self.user}"

    class Meta:
        # Add a unique constraint to ensure one like or dislike per user per prompt
        constraints = [
            UniqueConstraint(fields=["prompt", "user"], name="unique_like_dislike")
        ]


class ParameterMapping(Base):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, null=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True)
    parameter = models.ForeignKey(Parameter, on_delete=models.SET_NULL, null=True)
    value = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.parameter} - {self.model}"


class PromptVariable(Base):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, null=True, related_name='variables')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    value = models.CharField(max_length=256)
    key = models.CharField(max_length=256)


class PromptOutput(Base):
    prompt = models.ForeignKey(
        Prompt, on_delete=models.CASCADE, null=True, related_name="prompt_output"
    )
    output = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)

    def __str__(self):
        return f"output - {self.prompt}"
