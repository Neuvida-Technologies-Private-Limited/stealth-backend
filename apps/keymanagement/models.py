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
    )
    title = models.TextField(default="")
    description = models.TextField(default="")
    user = models.ForeignKey(User, related_name="keys", on_delete=models.CASCADE)
    api_key = EncryptedTextField()

    def mask_api_key(self):
        if len(self.api_key) >= 4:
            masked_part = '*' * (len(self.api_key) - 4)
            return self.api_key[:4] + masked_part
        else:
            # Handle cases where the API key is shorter than 4 characters
            return self.api_key

    def save(self, **kwargs) -> None:
        return super().save(**kwargs)
