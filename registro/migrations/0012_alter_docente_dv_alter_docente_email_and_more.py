# Generated by Django 4.1.1 on 2022-10-09 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registro', '0011_docente_estudiante_remove_profile_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docente',
            name='dv',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='digito verificador docente'),
        ),
        migrations.AlterField(
            model_name='docente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email docente'),
        ),
        migrations.AlterField(
            model_name='docente',
            name='estado',
            field=models.CharField(blank=True, default='activo', max_length=100, null=True, verbose_name='Estado docente'),
        ),
        migrations.AlterField(
            model_name='docente',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='nombre docente'),
        ),
        migrations.AlterField(
            model_name='docente',
            name='rut',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True, verbose_name='rut docente'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='dv',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='digito verificador estudiante'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email estudiante'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='estado',
            field=models.CharField(blank=True, default='activo', max_length=100, null=True, verbose_name='estado estudiante'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='nombre estudiante'),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='rut',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True, verbose_name='rut estudiante'),
        ),
        migrations.CreateModel(
            name='Coordinador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='nombre coordinador')),
                ('rut', models.CharField(blank=True, max_length=8, null=True, unique=True, verbose_name='rut coordinador')),
                ('dv', models.CharField(blank=True, max_length=1, null=True, verbose_name='digito verificador coordinador')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email coordinador')),
                ('estado', models.CharField(blank=True, default='activo', max_length=100, null=True, verbose_name='Estado coordinador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Coordinador',
                'verbose_name_plural': 'Coordinadores',
                'ordering': ['nombre'],
            },
        ),
    ]