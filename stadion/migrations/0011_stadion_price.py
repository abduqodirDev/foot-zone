# Generated by Django 5.1.3 on 2025-01-12 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stadion', '0010_stadionprice_unique_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='stadion',
            name='price',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Stadion narxi'),
        ),
    ]
