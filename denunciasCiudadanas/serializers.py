from rest_framework import serializers
from denunciasCiudadanas.models import Cuenta, Denuncia, Departamento, Municipio

class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields=("usuario_id", "tipo", "dui")

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
        
