# Generated by Django 4.1.1 on 2022-12-02 02:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nutricion', '0015_calificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_atencion',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Fecha Creación'),
            preserve_default=False,
        ),
    ]
