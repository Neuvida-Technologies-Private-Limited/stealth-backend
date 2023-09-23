import uuid
from enum import Enum

from django.db import models
from fernet_fields import EncryptedTextField

from apps.access.models import User


class LLMProviders(Enum):
    OPENAI = "OpenAI"
    BARD = "Bard"
    # Add more providers as needed


class KeyManagement(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(
        max_length=64,
        choices=[(choice.value, choice.name) for choice in LLMProviders],
        default=LLMProviders.OPENAI.value,
    )
    title = models.TextField(default="")
    description = models.TextField(default="")
    user = models.ForeignKey(User, related_name="keys", on_delete=models.CASCADE)
    api_key = EncryptedTextField()

    def save(self, **kwargs) -> None:
        return super().save(**kwargs)
