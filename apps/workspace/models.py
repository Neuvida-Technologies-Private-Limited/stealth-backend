import datetime
import uuid

from django.db import models
from django.utils import timezone

from apps.core.models import Base, Ownable
from apps.keymanagement.models import KeyManagement


class Workspace(Ownable, Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)  # Title of the workspace
    model_key = models.ForeignKey(
        KeyManagement, on_delete=models.SET_NULL, related_name="workspaces", null=True
    )
    last_modified = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.last_modified = timezone.now()
        return super().save(*args, **kwargs)
