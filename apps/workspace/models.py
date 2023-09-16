from django.db import models

from apps.core.models import Base, Ownable

class Workspace(Base, Ownable):
    title = models.CharField(max_length=255)  # Title of the workspace
    model_key = models.CharField(max_length=255)  # Key for the workspace model

    def __str__(self):
        return self.title