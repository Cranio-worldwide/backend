# Generated by Django 4.1.4 on 2023-06-20 08:51

import apps.specialists.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='Currency slug')),
                ('name', models.CharField(max_length=20, verbose_name='Currency name')),
                ('name_en', models.CharField(max_length=20, null=True, verbose_name='Currency name')),
                ('name_ru', models.CharField(max_length=20, null=True, verbose_name='Currency name')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
            ],
            options={
                'verbose_name': 'Specialist',
                'verbose_name_plural': 'Specialists',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.customuser',),
        ),
        migrations.CreateModel(
            name='SpecialistProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='First name')),
                ('first_name_en', models.CharField(blank=True, max_length=150, null=True, verbose_name='First name')),
                ('first_name_ru', models.CharField(blank=True, max_length=150, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='Last name')),
                ('last_name_en', models.CharField(blank=True, max_length=150, null=True, verbose_name='Last name')),
                ('last_name_ru', models.CharField(blank=True, max_length=150, null=True, verbose_name='Last name')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photo/%Y-%m-%d', verbose_name="Specialist's photo")),
                ('about', models.TextField(blank=True, verbose_name='About specialist')),
                ('about_en', models.TextField(blank=True, null=True, verbose_name='About specialist')),
                ('about_ru', models.TextField(blank=True, null=True, verbose_name='About specialist')),
                ('phone', models.CharField(blank=True, max_length=17, null=True, unique=True, verbose_name='Phone number')),
                ('practice_start', models.PositiveSmallIntegerField(blank=True, null=True, validators=[apps.specialists.validators.validate_year], verbose_name='Year of practice start')),
                ('diploma_issuer', models.CharField(blank=True, max_length=255, verbose_name='Organization-issuer of diploma')),
                ('diploma_recipient', models.CharField(blank=True, max_length=100, verbose_name='Name of diploma recipient mentioned in diploma')),
                ('status', models.CharField(choices=[('FILLING', 'application should be filled in'), ('CHECKING', 'pending diploma confirmation'), ('CORRECTING', 'application should be amended'), ('PAYMENT', 'pending payment'), ('ACTIVE', 'active therapist')], default='FILLING', max_length=50, verbose_name='Status of specialist')),
                ('specialist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Specialist Profile',
                'verbose_name_plural': 'Specialists Profiles',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_service', models.CharField(max_length=100, verbose_name='Service name')),
                ('name_service_en', models.CharField(max_length=100, null=True, verbose_name='Service name')),
                ('name_service_ru', models.CharField(max_length=100, null=True, verbose_name='Service name')),
                ('description', models.TextField(blank=True, verbose_name='Service detailed description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Service detailed description')),
                ('description_ru', models.TextField(blank=True, null=True, verbose_name='Service detailed description')),
                ('price', models.PositiveIntegerField(verbose_name='Sevice price')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='specialists.currency')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='specialists.specialist')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'ordering': ('currency', 'price'),
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_latitude', models.FloatField(verbose_name='Address latitude')),
                ('loc_longitude', models.FloatField(verbose_name='Address longitude')),
                ('description', models.TextField(blank=True, verbose_name='Details of address')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Details of address')),
                ('description_ru', models.TextField(blank=True, null=True, verbose_name='Details of address')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='specialists.specialist')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
