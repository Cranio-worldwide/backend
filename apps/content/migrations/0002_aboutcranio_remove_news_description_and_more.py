# Generated by Django 4.1.4 on 2023-07-03 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutCranio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='about_cranio/%Y-%m-%d', verbose_name='Picture')),
                ('text', models.TextField(verbose_name='About')),
                ('text_en', models.TextField(null=True, verbose_name='About')),
                ('text_ru', models.TextField(null=True, verbose_name='About')),
                ('link', models.URLField(verbose_name='Link')),
                ('is_published', models.BooleanField(default=True, verbose_name='Show on main page')),
            ],
        ),
        migrations.RemoveField(
            model_name='news',
            name='description',
        ),
        migrations.RemoveField(
            model_name='news',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='news',
            name='description_ru',
        ),
        migrations.RemoveField(
            model_name='news',
            name='published',
        ),
        migrations.AddField(
            model_name='news',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Show on site'),
        ),
        migrations.AddField(
            model_name='news',
            name='text',
            field=models.TextField(default='text', verbose_name='News text'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='text_en',
            field=models.TextField(null=True, verbose_name='News text'),
        ),
        migrations.AddField(
            model_name='news',
            name='text_ru',
            field=models.TextField(null=True, verbose_name='News text'),
        ),
        migrations.AddField(
            model_name='news',
            name='title',
            field=models.CharField(default='title', max_length=250, verbose_name='News title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='news',
            name='title_en',
            field=models.CharField(max_length=250, null=True, verbose_name='News title'),
        ),
        migrations.AddField(
            model_name='news',
            name='title_ru',
            field=models.CharField(max_length=250, null=True, verbose_name='News title'),
        ),
        migrations.AlterField(
            model_name='news',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Date of publishment'),
        ),
        migrations.AlterField(
            model_name='news',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='news/%Y-%m-%d', verbose_name='Picture'),
        ),
    ]
