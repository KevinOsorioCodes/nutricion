# Generated by Django 4.1.1 on 2022-10-18 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutricion', '0006_alter_detalle_atencion_prom_pliegue_abd_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle_atencion',
            name='estatura',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='detalle_atencion',
            name='peso_prom',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
