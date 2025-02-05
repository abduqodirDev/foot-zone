from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from core.settings import OTP_TIME
from users.managers import CustomManager
from users.validators import check_phone_validator, check_code_validator

USER, STADIONADMIN, SUPERADMIN = ("C", "A", "S")
class User(AbstractUser):
    USERROLE = (
        ("C", "COMMON-USER"),
        ("A", "STADIONADMIN"),
        ("S", "SUPERADMIN"),
    )

    phone_number = models.CharField(max_length=20, unique=True, validators=[check_phone_validator,])
    photo = models.ImageField(upload_to="user/", null=True, blank=True,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
                              ],
                              default="user/default.jpg",
                              verbose_name="Foydalanuvchi rasmi")
    role = models.CharField(max_length=20, choices=USERROLE, default='C')
    username = None
    USERNAME_FIELD = "phone_number"
    objects = CustomManager()


class VerificationOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verificationotps')

    code = models.CharField(max_length=4, validators=[check_code_validator])
    expires_time = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_time:
            self.expires_time = datetime.now() + timedelta(minutes=OTP_TIME)

        super(VerificationOtp, self).save(*args, **kwargs)

    def __str__(self):
        return f"OTP code for {self.user}"

    class Meta:
        verbose_name = 'Verification OTP'
        verbose_name_plural = 'Verification OTP'
        db_table = 'verifyotp'


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, validators=[check_phone_validator,])
    is_active = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="phone_numbers")

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        if PhoneNumber.objects.count() >= 3:
            raise ValidationError("Siz faqat 3 ta nomer qo‘shishingiz mumkin.")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Phone number'
        verbose_name_plural = 'Phone numbers'
        db_table = 'phone_number'
