from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import os
from django.core.exceptions import ValidationError
from urllib2 import urlopen
import json

def validate_file_extension(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.jpg','.png','.bmp','.mp4', '.avi']
  if not ext in valid_extensions:
    raise ValidationError(u'Solo se aceptan imagenes jpg, png o bmp, y videos mp4 o avi.')



#Distintos tipos de usuario
class Cuenta(models.Model):
    """Cuentas que realizan las denuncias"""
    ADMIN = '0'
    AGENTE = '1'
    CIUDADANO = '2'
    TIPO_DE_CUENTA=(
        (ADMIN,'Administrador del sistema'),
        (AGENTE, 'Agente investigador'),
        (CIUDADANO, 'Ciudadano'),
        )
    usuario=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    tipo=models.CharField(max_length=1, choices=TIPO_DE_CUENTA, default=CIUDADANO,)
    dui=models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.usuario.username

class Departamento (models.Model):
  nombre=models.CharField(max_length=25)
  def __str__(self):
    return self.nombre

class Municipio (models.Model):
  nombre=models.CharField(max_length=50)
  departamento=models.ForeignKey('Departamento',on_delete=models.CASCADE,)
  cuentaDenuncia=models.IntegerField(default=0)
  class Meta:
    unique_together=(("nombre", "departamento"),)
  def __str__(self):
    return self.nombre
    
class Denuncia(models.Model):
    """Denuncias Ciudadanas"""
    RECIBIDA = 'RE'
    ACEPTADA = 'AC'
    INVESTIGACION = 'IN'
    DOCUMENTADA = 'DO'
    PROCESADA = 'PR'
    CERRADA = 'CE'
    DENEGADA = 'DE'
    ESTADOS_CHOICES= (
        (RECIBIDA, 'Recibida'),
        (ACEPTADA, 'Aceptada'),
        (INVESTIGACION, 'Investigacion'),
        (DOCUMENTADA, 'Documentada'),
        (PROCESADA, 'Procesada'),
        (CERRADA, 'Cerrada'),
        (DENEGADA, 'Denegada'),
        )

    ROBO = 'RO'
    ASESINATO = 'AS'
    INCENDIO = 'IN'
    INUNDACION = 'IU'
    PLEITO = 'PL'
    ACTO_INMORAL = 'AI'
    OTROS = 'OT'

    CATEGORIA = (
        (ROBO, 'Robo'),
        (ASESINATO, 'Asesinato'),
        (INCENDIO, 'Incendio'),
        (INUNDACION, 'Inundacion'),
        (PLEITO, 'Pleito en lugar publico'),
        (ACTO_INMORAL, 'Acto inmoral'),
        (OTROS, 'Otros'),
        )
    
    titulo=models.CharField(max_length=50)
    descripcion = models.CharField(max_length=1000)
    cuenta=models.ForeignKey('Cuenta', on_delete=models.CASCADE,)
    ubicacionGeo=models.CharField(max_length=50)
    ubicacionGeoRef=models.CharField(max_length=50)
    municipio=models.ForeignKey('Municipio',on_delete=models.CASCADE,)
    prueba=models.FileField(upload_to='pruebas/%Y/%m/%d', blank=True, validators=[validate_file_extension])
    fecha=models.DateTimeField(default=timezone.now)
    estado= models.CharField(max_length=2, choices=ESTADOS_CHOICES, default=RECIBIDA,)
    categoria = models.CharField(max_length=2, choices=CATEGORIA, default=ROBO,)
    def __str__(self):
        return self.titulo

