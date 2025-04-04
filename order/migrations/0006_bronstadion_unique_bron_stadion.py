# Generated by Django 5.1.3 on 2024-12-11 04:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_bronstadion_status'),
        ('stadion', '0004_stadion_unique_user_for_stadium'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='bronstadion',
            constraint=models.UniqueConstraint(fields=('time', 'date', 'status', 'is_active'), name='unique_bron_stadion'),
        ),
    ]
