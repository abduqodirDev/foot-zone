# Generated by Django 5.1.3 on 2025-02-09 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tuman',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='viloyat',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
