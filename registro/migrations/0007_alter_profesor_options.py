# Generated by Django 4.1.1 on 2022-10-05 18:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0006_profesor_alumno'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profesor',
            options={'ordering': ['nombre'], 'verbose_name': 'profesor', 'verbose_name_plural': 'profesores'},
        ),
    ]
