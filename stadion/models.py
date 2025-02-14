from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.html import format_html
from rest_framework.exceptions import ValidationError

from utils.models import Viloyat, Tuman
from users.models import User


class Stadion(models.Model):
    title = models.CharField(max_length=200, verbose_name="Stadion nomi")
    description = models.TextField(verbose_name="Stadion haqida")
    price = models.PositiveBigIntegerField(verbose_name="Stadion narxi", default=0)
    photo = models.ImageField(upload_to="stadion/", null=True, blank=True,
                        validators=[
                                FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
                              ],
                        default="stadion/default.jpg",
                        verbose_name="Asosiy rasm",
                        help_text="Bu saytda asosiy rasm sifatida turadi")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="stadions")

    address = models.CharField(max_length=300, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    viloyat = models.ForeignKey(Viloyat, on_delete=models.SET_NULL, blank=True, null=True)
    tuman = models.ForeignKey(Tuman, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    kiyinish_xonasi = models.BooleanField(default=False)
    dush = models.BooleanField(default=False)
    yoritish = models.BooleanField(default=False)
    parkofka = models.BooleanField(default=False)
    forma = models.BooleanField(default=False)
    tishli_oyoqkiyim = models.BooleanField(default=False)
    usti_ochiq_yopiq = models.BooleanField(default=False)

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

    def save(self, *args, **kwargs):
        if self.stadion.images.count() > 5:
            raise ValidationError(detail="5 tadan ortiq rasm qo'sha ololmaysiz")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "image"
        verbose_name_plural = "images"
        db_table = "image"


class StadionPrice(models.Model):
    TIMES = (
        ('0', '00:00-01:00'),
        ('1', '01:00-02:00'),
        ('2', '02:00-03:00'),
        ('3', '03:00-04:00'),
        ('4', '04:00-05:00'),
        ('5', '05:00-06:00'),
        ('6', '06:00-07:00'),
        ('7', '07:00-08:00'),
        ('8', '08:00-09:00'),
        ('9', '09:00-10:00'),
        ('10', '10:00-11:00'),
        ('11', '11:00-12:00'),
        ('12', '12:00-13:00'),
        ('13', '13:00-14:00'),
        ('14', '14:00-15:00'),
        ('15', '15:00-16:00'),
        ('16', '16:00-17:00'),
        ('17', '17:00-18:00'),
        ('18', '18:00-19:00'),
        ('19', '19:00-20:00'),
        ('20', '20:00-21:00'),
        ('21', '21:00-22:00'),
        ('22', '22:00-23:00'),
        ('23', '23:00-00:00'),
    )

    time = models.CharField(max_length=2, choices=TIMES)
    price = models.PositiveIntegerField(default=0)
    stadion = models.ForeignKey(Stadion, on_delete=models.CASCADE, related_name='prices')

    def __str__(self):
        return f"{self.time} for {self.stadion}"

    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'
        db_table = 'price'
        constraints = [
            models.UniqueConstraint(fields=['stadion', 'time'], name='unique_price')
        ]


class StadionReview(models.Model):
    stadion = models.ForeignKey("Stadion", on_delete=models.SET_NULL, blank=True, null=True, related_name="stadionreviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} writed for {self.stadion}"

    class Meta:
        verbose_name = "Stadion sharhi"
        verbose_name_plural = "Stadion sharhlari"
        db_table = "stadion_review"
