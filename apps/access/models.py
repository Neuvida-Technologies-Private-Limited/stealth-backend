import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Your other user fields here

    # UUID field
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    token = models.CharField(default="", max_length=64)
    reset_password_token = models.CharField(default="", max_length=64)

    def __str__(self):
        return self.username
