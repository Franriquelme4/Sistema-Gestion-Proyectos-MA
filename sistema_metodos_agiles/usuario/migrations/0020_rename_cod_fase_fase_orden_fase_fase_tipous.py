# Generated by Django 4.1 on 2022-10-07 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0019_alter_fase_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fase',
            old_name='cod_fase',
            new_name='orden_fase',
        ),
        migrations.AddField(
            model_name='fase',
            name='tipoUs',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.tipouserstory'),
        ),
    ]