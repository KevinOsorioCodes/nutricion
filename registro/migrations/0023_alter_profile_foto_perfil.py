# Generated by Django 4.1.1 on 2022-11-14 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0022_alter_discapacidad_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='foto_perfil',
            field=models.ImageField(default='no-avatar.jpg', null=True, upload_to='fotos_perfil/'),
        ),
    ]
