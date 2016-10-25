from rest_framework import serializers
from denunciasCiudadanas.models import Cuenta, Denuncia

class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields=("usuario_id", "tipo")

class DenunciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denuncia
        fields=("titulo", "descripcion", "cuenta",
                "categoria", "estado", "prueba",
                "ubicacionGeo", 'ubicacionGeoRef', "fecha")
