from django.db.models.signals import post_save
from django.dispatch import receiver

from stadion.models import Stadion, StadionPrice


@receiver(post_save, sender=Stadion)
def post_save_profile(sender, instance, created, *args, **kwargs):
    if created:
        for i in range(24):
            StadionPrice.objects.create(time=str(i), price=instance.price, stadion=instance)
