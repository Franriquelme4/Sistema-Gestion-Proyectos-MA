# Generated by Django 4.1 on 2022-10-07 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0020_rename_cod_fase_fase_orden_fase_fase_tipous'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUs_Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proyecto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.proyecto')),
                ('tipoUs', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.tipouserstory')),
            ],
        ),
    ]