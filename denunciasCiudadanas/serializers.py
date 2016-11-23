from rest_framework import serializers
from denunciasCiudadanas.models import Cuenta, Denuncia

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
