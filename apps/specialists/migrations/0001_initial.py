# Generated by Django 4.1.4 on 2023-08-18 19:23

import apps.specialists.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CranioInstitute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
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
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('title_en', models.CharField(max_length=100, null=True, unique=True)),
                ('title_ru', models.CharField(max_length=100, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('title_en', models.CharField(max_length=100, null=True, unique=True)),
                ('title_ru', models.CharField(max_length=100, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Type of services',
                'verbose_name_plural': 'Types of services',
            },
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('about', models.TextField(blank=True, verbose_name='About specialist')),
                ('about_en', models.TextField(blank=True, null=True, verbose_name='About specialist')),
                ('about_ru', models.TextField(blank=True, null=True, verbose_name='About specialist')),
                ('speciality', models.CharField(max_length=100, verbose_name='Speciality')),
                ('speciality_en', models.CharField(max_length=100, null=True, verbose_name='Speciality')),
                ('speciality_ru', models.CharField(max_length=100, null=True, verbose_name='Speciality')),
                ('languages', models.ManyToManyField(to='specialists.language')),
                ('service_types', models.ManyToManyField(to='specialists.servicetype')),
            ],
            options={
                'verbose_name': 'Specialist Profile',
                'verbose_name_plural': 'Specialists Profiles',
            },
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('title_en', models.CharField(max_length=100, null=True, unique=True)),
                ('title_ru', models.CharField(max_length=100, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Specialization',
                'verbose_name_plural': 'Specializations',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(choices=[('FILLING', 'Filling out the application.'), ('CHECK', 'Pending diploma confirmation.'), ('EDIT', 'Corrections are required.'), ('PAYING', 'Pending payment.'), ('ACTIVE', 'Active account.')], default='FILLING', max_length=50, verbose_name='Status of specialist')),
                ('comments', models.TextField(blank=True, verbose_name='Admin comments for corrections')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Last status update')),
                ('specialist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='status', to='specialists.specialist')),
            ],
            options={
                'verbose_name': 'Specialist Status',
                'verbose_name_plural': 'Specialists Statuses',
            },
        ),
        migrations.AddField(
            model_name='specialist',
            name='specializations',
            field=models.ManyToManyField(to='specialists.specialization'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='diplomas/%Y-%m-%d', verbose_name='Scanned document')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='specialists.specialist')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='CranioDiploma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.SmallIntegerField(validators=[apps.specialists.validators.validate_year], verbose_name='Year of diploma issue')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='specialists.cranioinstitute')),
                ('scan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='specialists.document')),
                ('specialist', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='diploma', to='specialists.specialist')),
            ],
            options={
                'verbose_name': 'Education data',
                'verbose_name_plural': 'Education datas',
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
                ('min_price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Value should be larger than 0.')], verbose_name='Minimal price')),
                ('currency', models.ForeignKey(default=3, on_delete=django.db.models.deletion.SET_DEFAULT, to='specialists.currency', verbose_name='Currency')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='specialists.specialist')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
