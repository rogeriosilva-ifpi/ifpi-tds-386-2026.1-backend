from rest_framework.serializers import ModelSerializer
from .models import Selecao, Sede


class SelecaoSerializer(ModelSerializer):
    
    class Meta:
        model = Selecao
        fields = ['id', 'pais', 'tecnico', 'grupo_fase1']


class SedeSerializer(ModelSerializer):

    class Meta:
        model = Sede
        fields = '__all__'