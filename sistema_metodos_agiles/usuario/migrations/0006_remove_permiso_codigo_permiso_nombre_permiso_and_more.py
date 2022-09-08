# Generated by Django 4.1 on 2022-09-08 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0005_permiso_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permiso',
            name='codigo',
        ),
        migrations.AddField(
            model_name='permiso',
            name='nombre_permiso',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rol',
            name='nombre_rol',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]