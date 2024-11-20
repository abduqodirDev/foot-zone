from django.db import models


class ActiveBronStadionManager(models.Manager):
    def get_queryset(self):
        from order.models import TASDIQLANGAN
        return super().get_queryset().filter(status=TASDIQLANGAN, is_active=True)

