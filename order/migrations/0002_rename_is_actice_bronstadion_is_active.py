# Generated by Django 5.1.3 on 2024-11-18 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bronstadion',
            old_name='is_actice',
            new_name='is_active',
        ),
    ]
