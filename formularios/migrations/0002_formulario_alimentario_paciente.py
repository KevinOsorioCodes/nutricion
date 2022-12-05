# Generated by Django 4.1.1 on 2022-11-09 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0022_alter_discapacidad_options'),
        ('formularios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario_alimentario',
            name='paciente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='registro.paciente'),
            preserve_default=False,
        ),
    ]