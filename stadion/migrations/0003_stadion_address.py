# Generated by Django 5.1.3 on 2024-11-19 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stadion', '0002_rename_created_time_stadion_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stadion',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
