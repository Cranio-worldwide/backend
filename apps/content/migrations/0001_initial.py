# Generated by Django 4.1.4 on 2023-06-17 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            name='StaticContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField()),
                ('fields_ru', models.JSONField()),
                ('fields_en', models.JSONField()),
            ],
        ),
    ]
