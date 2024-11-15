from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.validators import MinValueValidator, MaxValueValidator

from common.models import BaseModel


class Stadion(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Stadion nomi")
    description = models.TextField(verbose_name="Stadion haqida")
    price = models.FloatField(verbose_name="Stadion narxi")
    photo = models.ImageField(upload_to="stadion/", null=True, blank=True,
                        validators=[
                                FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
                              ],
                        verbose_name="Asosiy rasm",
                        help_text="Bu saytda asosiy rasm sifatida turadi")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stadions")

    start_time = models.TimeField(null=True, blank=True, help_text="Stadion boshlanish vaqti")
    end_time = models.TimeField(null=True, blank=True, help_text="Stadion tugash vaqti")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    kiyinish_xonasi = models.BooleanField(default=False)
    dush = models.BooleanField(default=False)
    yoritish = models.BooleanField(default=False)
    parkofka = models.BooleanField(default=False)
    forma = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Stadion'
        verbose_name_plural = 'Stadionlar'
        db_table = "stadion"


class Images(models.Model):
    stadion = models.ForeignKey('Stadion', on_delete=models.CASCADE, related_name="images")

    image = models.ImageField(upload_to="stadion/", null=True, blank=True,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
                              ])

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="100" />', self.image.url)
        return "Rasm mavjud emas"

    image_tag.short_description = 'Stadion rasmi'

    def __str__(self):
        return f"{self.id} : {self.stadion.title}"

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"
        db_table = "image"


class StadionReview(models.Model):
    stadion = models.ForeignKey("Stadion", on_delete=models.CASCADE, related_name="stadionreviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.TextField()
    rank = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} writed for {self.stadion}"

    class Meta:
        verbose_name = "Stadion sharhi"
        verbose_name_plural = "Stadion sharhlari"
        db_table = "stadion_review"
