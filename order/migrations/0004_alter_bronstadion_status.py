# Generated by Django 5.1.3 on 2024-11-21 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_bronstadion_created_at_bronstadion_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bronstadion',
            name='status',
            field=models.CharField(choices=[('T', 'TASDIQLANGAN'), ('F', 'TASDIQLANMAGAN')], default='F', max_length=20),
        ),
    ]