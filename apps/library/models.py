from django.db import models
from django.db.models import UniqueConstraint

from apps.core.models import Base, Ownable
from apps.prompt.models import Prompt

# Create your models here.
class LikeDislike(Base, Ownable):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name='likes_dislikes')  # Related prompt
    liked = models.BooleanField(default=True)  # True for like, False for dislike

    def __str__(self):
        status = 'Liked' if self.liked else 'Disliked'
        return f"{status}: {self.user}"

    class Meta:
        # Add a unique constraint to ensure one like or dislike per user per prompt
        constraints = [
            UniqueConstraint(fields=['prompt', 'user'], name='unique_like_dislike')
        ]
