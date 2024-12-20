import uuid

from django.db import models

from stadion.models import Stadion
from users.models import User


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LikedStadion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserLikedStadion')
    stadion = models.ForeignKey(Stadion, on_delete=models.CASCADE, related_name='StadionLikedStadion')

    class Meta:
        verbose_name = 'LikedStadion'
        verbose_name_plural = 'LikedStadions'
        db_table = 'likedstadion'
