from django.db import models
from apps.core.models import Ownable, Base, Generic

# Create your models here.
class KeyManagement(Base, Ownable, Generic):
    title = models.CharField(max_length=64)
    api_key = models.CharField(max_length=512)