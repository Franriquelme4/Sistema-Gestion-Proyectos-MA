# Generated by Django 4.1 on 2022-09-26 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_tablero_proyecto_sprint'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='id_sprints',
            field=models.ManyToManyField(blank=True, to='usuario.sprint'),
        ),
    ]
