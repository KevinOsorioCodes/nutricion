# Generated by Django 4.1.1 on 2022-11-15 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0024_alter_profile_foto_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinador',
            name='nombre',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='nombre coordinador'),
        ),
        migrations.AlterField(
            model_name='docente',
            name='nombre',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='nombre docente'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='nombre',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='nombre estudiante'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nombre',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre Paciente'),
        ),
    ]
