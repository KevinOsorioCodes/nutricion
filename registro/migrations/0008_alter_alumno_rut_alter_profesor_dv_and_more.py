# Generated by Django 4.1.1 on 2022-10-05 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0007_alter_profesor_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='rut',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True, verbose_name='rut alumno'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='dv',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='digito verificador profesor'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='estado',
            field=models.CharField(blank=True, default='activo', max_length=100, null=True, verbose_name='Estado profesor'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='nombre profesor'),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='rut',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True, verbose_name='rut profesor'),
        ),
    ]