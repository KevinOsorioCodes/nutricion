# Generated by Django 4.1.1 on 2022-10-18 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0020_rename_fecha_naciemiento_paciente_fecha_nacimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='genero',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Genero paciente'),
        ),
    ]
