# Generated by Django 4.1.1 on 2022-10-25 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutricion', '0009_remove_solicitud_atencion_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='fecha_eval',
            field=models.DateField(verbose_name='Fecha atencion'),
        ),
    ]
