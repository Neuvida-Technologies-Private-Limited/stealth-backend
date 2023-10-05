import uuid
from enum import Enum
from cryptography.fernet import Fernet

from django.db import models
from fernet_fields import EncryptedTextField

from apps.access.models import User
from apps.core.models import Base

class LLMProviders(Enum):
    OPENAI = "OpenAI"
    BARD = "Bard"
    # Add more providers as needed


class KeyManagement(Base):
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
            # Create a random encryption key
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            masked_bytes = cipher_suite.encrypt(self.api_key[4:].encode())
            # Concatenate the first 4 characters and the encrypted part
            masked_string = self.api_key[:4] + masked_bytes.decode()
            masked_part = '*' * (len(masked_string) - 4)
            return self.api_key[:4] + masked_part
        else:
            # Handle cases where the API key is shorter than 4 characters
            return self.api_key

    def save(self, **kwargs) -> None:
        return super().save(**kwargs)
