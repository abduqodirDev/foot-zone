# Generated by Django 5.1.3 on 2025-01-10 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stadion', '0007_stadionprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stadion',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='stadion',
            name='price',
        ),
        migrations.RemoveField(
            model_name='stadion',
            name='start_time',
        ),
    ]
