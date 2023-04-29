# Generated by Django 4.1.4 on 2023-04-09 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('loc_longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('description', models.TextField(blank=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('description_ru', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('description_en', models.TextField(null=True)),
                ('description_ru', models.TextField(null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='news/%Y-%m-%d')),
                ('date', models.DateField(auto_now_add=True)),
                ('published', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_service', models.CharField(default="Specialist's appointment", max_length=80)),
                ('name_service_en', models.CharField(default="Specialist's appointment", max_length=80, null=True)),
                ('name_service_ru', models.CharField(default="Specialist's appointment", max_length=80, null=True)),
                ('description', models.TextField(blank=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('description_ru', models.TextField(blank=True, null=True)),
                ('price', models.PositiveIntegerField()),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('RUB', 'RUB')], default='USD', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='StaticContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('fields_ru', models.JSONField()),
                ('fields_en', models.JSONField()),
            ],
        ),
    ]
