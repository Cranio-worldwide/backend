# Generated by Django 4.1.4 on 2023-03-25 09:34

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
                ('loc_latitude', models.DecimalField(decimal_places=6, max_digits=8)),
                ('loc_longitude', models.DecimalField(decimal_places=6, max_digits=8)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_service', models.CharField(default='visiting a specialist', max_length=80)),
                ('description', models.TextField(blank=True)),
                ('price', models.PositiveIntegerField()),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('RUB', 'RUB')], default='USD', max_length=50)),
            ],
        ),
    ]