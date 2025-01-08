# Generated by Django 5.1.3 on 2025-01-08 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_username_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('C', 'COMMON-USER'), ('A', 'STADIONADMIN'), ('S', 'SUPERADMIN')], default='C', max_length=20),
        ),
    ]