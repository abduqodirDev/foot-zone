from django.db import models


class Viloyat(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Viloyat'
        verbose_name_plural = 'Viloyatlar'
        db_table = "viloyat"


class Tuman(models.Model):
    name = models.CharField(max_length=50)

    viloyat = models.ForeignKey(Viloyat, on_delete=models.CASCADE, related_name="tumanlar")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tuman"
        verbose_name_plural = "Tumanlar"
        db_table = "tuman"
