# Generated by Django 4.1 on 2022-10-06 19:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0013_remove_userstory_prioridadtec_us_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='fecha_creacion',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='tipouserstory',
            name='fecha_creacion',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='userstory',
            name='fecha_creacion',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
