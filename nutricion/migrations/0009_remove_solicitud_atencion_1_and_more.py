# Generated by Django 4.1.1 on 2022-10-25 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0022_alter_discapacidad_options'),
        ('nutricion', '0008_detalle_atencion_estudiante'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud',
            name='atencion_1',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='atencion_2',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='atencion_3',
        ),
        migrations.RemoveField(
            model_name='solicitud',
            name='created',
        ),
        migrations.AddField(
            model_name='solicitud',
            name='estudiante',
            field=models.ManyToManyField(related_name='estudiante', to='registro.estudiante'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='fecha_eval',
            field=models.DateTimeField(auto_now_add=True, default="2022-10-25", verbose_name='Fecha atencion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitud',
            name='paciente',
            field=models.ManyToManyField(related_name='paciente', to='registro.paciente'),
        ),
    ]
