from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from users.managers import CustomManager
from users.validators import check_phone_validator


USER, STADIONADMIN, SUPERADMIN = ("USER", "STADIONADMIN", "SUPERUSER")
class User(AbstractUser):
    USERROLE = (
        ("C", "COMMON-USER"),
        ("A", "STADIONADMIN"),
        ("S", "SUPERUSER"),
    )

    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[check_phone_validator,])
    photo = models.ImageField(upload_to="user/", null=True, blank=True,
                              validators=[
                                  FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
                              ],
                              default="user/default.jpg",
                              verbose_name="Foydalanuvchi rasmi")
    role = models.CharField(max_length=20, choices=USERROLE, default='C')

    objects = CustomManager()

