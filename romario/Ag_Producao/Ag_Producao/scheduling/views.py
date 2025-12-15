# views.py

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpRequest, JsonResponse
from .models import TarefaProducao

# Função simples de otimização (pode ser expandida conforme necessário)
def otimizar_agendamento(tarefas):
    # Aqui você pode colocar a lógica do seu algoritmo de otimização.
    # Este exemplo só vai ordenar as tarefas por prioridade e tempo estimado.
    return sorted(tarefas, key=lambda x: (x.prioridade, x.tempo_estimado))

@api_view(["GET", "POST"])
def optimize(request: HttpRequest) -> Response:
    if request.method == "GET":
        # Resposta simples para o método GET
        return JsonResponse({"message": "Bem-vindo ao ScheduleAI!"})
    
    elif request.method == "POST":
        # Recebe os dados do corpo da requisição (formato JSON)
        try:
            dados = request.data  # Exemplo: [{"nome_produto": "Produto A", "quantidade": 10, "tempo_estimado": 2.5}]
            
            # Verificando se o corpo da requisição contém os dados necessários
            if not dados:
                return JsonResponse({"error": "Nenhum dado de produção fornecido."}, status=400)
            
            # Processar os dados de produção (simulando inserção no banco de dados)
            tarefas = []
            for item in dados:
                tarefa = TarefaProducao(
                    nome_produto=item["nome_produto"],
                    quantidade=item["quantidade"],
                    tempo_estimado=item["tempo_estimado"],
                    prioridade=item.get("prioridade", 1),  # A prioridade pode ser opcional
                )
                tarefa.save()  # Salva a tarefa no banco de dados
                tarefas.append(tarefa)

            # Agora, vamos otimizar o agendamento usando o algoritmo
            tarefas_otimizadas = otimizar_agendamento(tarefas)

            # Preparar a resposta com os dados otimizados
            resposta = []
            for tarefa in tarefas_otimizadas:
                resposta.append({
                    "nome_produto": tarefa.nome_produto,
                    "quantidade": tarefa.quantidade,
                    "tempo_estimado": tarefa.tempo_estimado,
                    "prioridade": tarefa.prioridade,
                })

            return JsonResponse({"agendamento_otimizado": resposta}, status=200)
        
        except Exception as e:
            return JsonResponse({"error": f"Ocorreu um erro: {str(e)}"}, status=500)
