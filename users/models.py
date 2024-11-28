from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from core.settings import OTP_TIME
from users.managers import CustomManager
from users.validators import check_phone_validator, check_code_validator

USER, STADIONADMIN, SUPERADMIN = ("USER", "STADIONADMIN", "SUPERUSER")
class User(AbstractUser):
    USERROLE = (
        ("C", "COMMON-USER"),
        ("A", "STADIONADMIN"),
        ("S", "SUPERUSER"),
    )

    SEX = (
        ('E', 'ERKAK'),
        ('A', 'AYOL')
    )

    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[check_phone_validator,])
    photo = models.ImageField(upload_to="user/", null=True, blank=True,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
                              ],
                              default="user/default.jpg",
                              verbose_name="Foydalanuvchi rasmi")
    role = models.CharField(max_length=20, choices=USERROLE, default='C')
    middle_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="Otasining ismi")
    date_of_birth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=2, choices=SEX, null=True, blank=True)

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
