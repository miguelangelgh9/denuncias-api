# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User
from denunciasCiudadanas.models import Cuenta, Denuncia, Departamento, Municipio

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("username", "first_name", "last_name", "email")

class CuentaSerializer(serializers.ModelSerializer):
    usuario=UsuarioSerializer()
    class Meta:
        model = Cuenta
        fields=("usuario_id", "usuario", "tipo", "dui")

class DenunciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denuncia
        fields=("id", "titulo", "descripcion", "cuenta",
                "categoria", "estado", "prueba", "municipio",
                "ubicacionGeo", 'ubicacionGeoRef', "fecha")

class FiltroDenunciaSerializer(DenunciaSerializer):
    model= Denuncia

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ("id", "nombre", "cuentaDenuncia")

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ('id', 'nombre')

class DepMunSerializer(serializers.ModelSerializer):
    departamento=DepartamentoSerializer()
    class Meta:
        model = Municipio
        fields = ('id', 'nombre', 'departamento')
        
class DenunciaActualSerializer(DenunciaSerializer):
    model=Denuncia
