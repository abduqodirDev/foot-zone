# Generated by Django 5.1.3 on 2024-12-20 17:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stadion', '0005_remove_stadion_unique_user_for_stadium'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LikedStadion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stadion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='StadionLikedStadion', to='stadion.stadion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserLikedStadion', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'LikedStadion',
                'verbose_name_plural': 'LikedStadions',
                'db_table': 'likedstadion',
            },
        ),
    ]
