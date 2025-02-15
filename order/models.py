from django.db import models

from stadion.models import Stadion
from users.models import User
from order.managers import ActiveBronStadionManager


KUTILMOQDA, TASDIQLANGAN, BEKOR_QILINGAN = ('K', 'T', 'B')
class BronStadion(models.Model):
    TIMECHOICE = (
        ("0", "00.00-01.00"),
        ("1", "01.00-02.00"),
        ("2", "02.00-03.00"),
        ("3", "03.00-04.00"),
        ("4", "04.00-05.00"),
        ("5", "05.00-06.00"),
        ("6", "06.00-07.00"),
        ("7", "07.00-08.00"),
        ("8", "08.00-09.00"),
        ("9", "09.00-10.00"),
        ("10", "10.00-11.00"),
        ("11", "11.00-12.00"),
        ("12", "12.00-13.00"),
        ("13", "13.00-14.00"),
        ("14", "14.00-15.00"),
        ("15", "15.00-16.00"),
        ("16", "16.00-17.00"),
        ("17", "17.00-18.00"),
        ("18", "18.00-19.00"),
        ("19", "19.00-20.00"),
        ("20", "20.00-21.00"),
        ("21", "21.00-22.00"),
        ("22", "22.00-23.00"),
        ("23", "23.00-00.00"),
    )

    STATUSCHOICE = (
        ("K", "KUTILMOQDA"),
        ("T", "TASDIQLANGAN"),
        ("B", "BEKOR_QILINGAN")
    )

    stadion = models.ForeignKey(Stadion, on_delete=models.CASCADE, related_name="stadion_bronorders", db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bronorders")

    time = models.CharField(max_length=20, choices=TIMECHOICE)
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUSCHOICE, default=KUTILMOQDA)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    ActiveBronStadion = ActiveBronStadionManager()

    def __str__(self):
        return f"{self.user} for {self.stadion}"

    class Meta:
        verbose_name = "Bron stadion"
        verbose_name_plural = "Bron stadionlar"
        db_table = "bronstadion"
        constraints = [
            models.UniqueConstraint(fields=['time', 'date', 'user', 'stadion'], name='unique_bron_stadion')
        ]
