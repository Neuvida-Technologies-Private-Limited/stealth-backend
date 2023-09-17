from collections.abc import Iterable
from enum import Enum
import uuid

from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet


class ProviderChoices(Enum):
    OPENAI = 'OpenAI'
    BARD = 'Bard'
    # Add more providers as needed

class KeyManagement(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        max_length=64,
        choices=[(choice.value, choice.name) for choice in ProviderChoices],
        default=ProviderChoices.OPENAI.value,
    )
    user = models.ForeignKey(User, related_name='keys', on_delete=models.CASCADE)
    api_key = models.CharField(max_length=1024)

    def save(self, **kwargs) -> None:
        return super().save(**kwargs)