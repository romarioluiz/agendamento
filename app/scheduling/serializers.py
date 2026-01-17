from rest_framework import serializers
from .models import TarefaProducao, Agendamento

class TarefaProducaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarefaProducao
        fields = ['id', 'nome', 'duracao', 'prioridade', 'deadline', 'created_at']
        read_only_fields = ['created_at']

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'
        read_only_fields = ['created_at', 'executado_em']