# Generated by Django 5.1.3 on 2024-11-18 10:36

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stadion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='stadion',
            old_name='created_time',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='stadion',
            name='updated_time',
        ),
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='stadion/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]),
        ),
        migrations.AlterField(
            model_name='stadion',
            name='dush',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stadion',
            name='forma',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stadion',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='stadion',
            name='kiyinish_xonasi',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stadion',
            name='parkofka',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stadion',
            name='photo',
            field=models.ImageField(blank=True, default='stadion/default.jpg', help_text='Bu saytda asosiy rasm sifatida turadi', null=True, upload_to='stadion/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='Asosiy rasm'),
        ),
        migrations.AlterField(
            model_name='stadion',
            name='price',
            field=models.PositiveBigIntegerField(verbose_name='Stadion narxi'),
        ),
        migrations.AlterField(
            model_name='stadion',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stadions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stadion',
            name='yoritish',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='StadionReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rank', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('stadion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stadionreviews', to='stadion.stadion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Stadion sharhi',
                'verbose_name_plural': 'Stadion sharhlari',
                'db_table': 'stadion_review',
            },
        ),
    ]
