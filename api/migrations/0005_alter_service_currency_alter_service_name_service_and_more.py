# Generated by Django 4.1.4 on 2023-04-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_specialists_id_address_specialist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('RUB', 'RUB')], default='USD', max_length=5),
        ),
        migrations.AlterField(
            model_name='service',
            name='name_service',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='service',
            name='name_service_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='name_service_ru',
            field=models.CharField(max_length=100, null=True),
        ),
    ]