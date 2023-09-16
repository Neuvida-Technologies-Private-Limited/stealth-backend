from django.db import models
from apps.core.models import Ownable, Base

# Create your models here.
class KeyManagement(Base, Ownable):
    title = models.CharField(max_length=64)
    api_key = models.CharField(max_length=512)