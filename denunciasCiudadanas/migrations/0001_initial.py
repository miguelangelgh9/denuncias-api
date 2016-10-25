# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-24 00:30
from __future__ import unicode_literals

import denunciasCiudadanas.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tipo', models.CharField(choices=[('0', 'Administrador del sistema'), ('1', 'Agente investigador'), ('2', 'Ciudadano')], default='2', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Denuncia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=1000)),
                ('ubicacionGeo', models.CharField(max_length=50)),
                ('ubicacionGeoRef', models.CharField(max_length=50)),
                ('prueba', models.FileField(blank=True, upload_to='pruebas/%Y/%m/%d', validators=[denunciasCiudadanas.models.validate_file_extension])),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('estado', models.CharField(choices=[('RE', 'Recibida'), ('AC', 'Aceptada'), ('IN', 'Investigacion'), ('DO', 'Documentada'), ('PR', 'Procesada'), ('CE', 'Cerrada'), ('DE', 'Denegada')], default='RE', max_length=2)),
                ('categoria', models.CharField(choices=[('RO', 'Robo'), ('AS', 'Asesinato'), ('IN', 'Incendio'), ('IU', 'Inundacion'), ('PL', 'Pleito en lugar publico'), ('AI', 'Acto inmoral'), ('OT', 'Otros')], default='RO', max_length=2)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='denunciasCiudadanas.Cuenta')),
            ],
        ),
    ]
