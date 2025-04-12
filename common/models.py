import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
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
        constraints = [
            models.UniqueConstraint(fields=['user', 'stadion'], name='unique_liked_stadion')
        ]


# class Starts(models.Model):
#     rank = models.IntegerField(validators=[
#         MinValueValidator(0),
#         MaxValueValidator(5)
#     ])
#     stadion = models.ForeignKey(Stadion, on_delete=models.CASCADE, related_name='StadionStarts')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserStarts')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.rank}"
#
#     class Meta:
#         verbose_name = 'Start'
#         verbose_name_plural = 'Starts'
#         db_table = 'starts'
