# Generated by Django 4.1.4 on 2023-04-08 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='specialists_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='users.specialist'),
        ),
        migrations.AddField(
            model_name='address',
            name='specialists_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='users.specialist'),
        ),
    ]
