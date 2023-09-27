from collections.abc import Iterable
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



class User(AbstractUser):
    # Your other user fields here

    # UUID field
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    token = models.CharField(default="", max_length=64, blank=True)
    reset_password_token = models.CharField(default="", max_length=64, blank=True)
    email = models.EmailField(_('email address'), blank=False, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Add any other required fields here

    class Meta:
        unique_together = ('id', 'uuid')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs) -> None:
        if not self.email:
            self.email = self.username
        if not self.username:
            self.username = self.email

        return super().save(*args, **kwargs)
