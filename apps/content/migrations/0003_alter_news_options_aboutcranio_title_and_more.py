# Generated by Django 4.1.4 on 2023-08-20 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_aboutcranio_remove_news_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('-date',), 'verbose_name': 'New', 'verbose_name_plural': 'News'},
        ),
        migrations.AddField(
            model_name='aboutcranio',
            name='title',
            field=models.CharField(default='About', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aboutcranio',
            name='title_en',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='aboutcranio',
            name='title_ru',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date of publishment'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='title_en',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='title_ru',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]