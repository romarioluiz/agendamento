from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import render
import json
import time

from .algorithms.busca import busca_local, busca_local_tempo, custo_multi_maquina
from .algorithms.sa import simulated_annealing
from .models import TarefaProducao, Agendamento

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def tarefa_list(request):
    """
    Lista todas as tarefas ou cria uma nova
    """
    if request.method == 'GET':
        tarefas = TarefaProducao.objects.all().values()
        return Response(list(tarefas))
    
    elif request.method == 'POST':
        try:
            nome = request.data.get('nome')
            duracao = request.data.get('duracao')
            deadline = request.data.get('deadline', 0)
            prioridade = request.data.get('prioridade', 1)
            
            if not nome or not duracao:
                return Response(
                    {"erro": "Nome e duração são obrigatórios"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            tarefa = TarefaProducao.objects.create(
                nome=nome,
                duracao=duracao,
                deadline=deadline,
                prioridade=prioridade
            )
            
            return Response({
                "id": tarefa.id,
                "nome": tarefa.nome,
                "duracao": tarefa.duracao,
                "deadline": tarefa.deadline,
                "prioridade": tarefa.prioridade,
                "mensagem": "Tarefa criada com sucesso"
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"erro": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(["POST"])
@permission_classes([AllowAny])
def optimize(request):
    """
    Endpoint responsável por otimizar o escalonamento de tarefas
    usando Busca Local ou Simulated Annealing.
    """
    try:
        # 1️⃣ Lê os parâmetros
        metodo = request.data.get("method", "busca")
        tarefas = request.data.get("tarefas", [])
        num_maquinas = request.data.get("num_maquinas", 3)
        max_iter = request.data.get("max_iter", 1000)
        objetivo = request.data.get("objetivo", "tempo")  # 'tempo' ou 'penalidade'
        
        # 2️⃣ Validação
        if not tarefas:
            return Response(
                {"erro": "Lista de tarefas vazia ou não enviada"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Converter para formato dos algoritmos
        tarefas_formatadas = []
        for i, tarefa in enumerate(tarefas):
            tarefas_formatadas.append({
                "id": tarefa.get("id", f"T{i+1}"),
                "nome": tarefa.get("nome", f"Tarefa {i+1}"),
                "tempo": tarefa.get("duracao", tarefa.get("tempo", 1)),
                "deadline": tarefa.get("deadline", 0)
            })
        
        # 3️⃣ Escolhe e executa o algoritmo
        inicio_tempo = time.time()
        
        if metodo == "sa":
            resultado = simulated_annealing(
                tarefas=tarefas_formatadas,
                num_maquinas=num_maquinas,
                max_iter=max_iter,
                objetivo=objetivo
            )
            
            solucao = resultado.get("solucao", [])
            custo = resultado.get("custo", 0)
            resultado_detalhado = resultado.get("resultado_detalhado", {})
            
        else:  # metodo == "busca" ou padrão
            if objetivo == "tempo":
                solucao, makespan = busca_local_tempo(
                    tarefas_formatadas,
                    max_iter=max_iter,
                    num_maquinas=num_maquinas
                )
                custo = makespan
                resultado_detalhado = custo_multi_maquina(solucao, num_maquinas)
            else:
                solucao, custo_resultado = busca_local(
                    tarefas_formatadas,
                    max_iter=max_iter,
                    num_maquinas=num_maquinas
                )
                custo = custo_resultado.get('custo_total', 0) if isinstance(custo_resultado, dict) else custo_resultado
                resultado_detalhado = custo_multi_maquina(solucao, num_maquinas)
        
        tempo_execucao = time.time() - inicio_tempo
        
        # 4️⃣ Calcular estatísticas
        tempos_maquinas = resultado_detalhado.get('tempos_maquinas', [])
        if not tempos_maquinas:
            # Calcular manualmente se necessário
            tempos_maquinas = [0] * num_maquinas
            for idx, tarefa in enumerate(solucao):
                maquina = idx % num_maquinas
                tempos_maquinas[maquina] += tarefa["tempo"]
        
        # 5️⃣ Salvar no banco de dados (opcional)
        try:
            agendamento = Agendamento.objects.create(
                nome=f"Agendamento {metodo.upper()}",
                algoritmo=metodo,
                num_maquinas=num_maquinas,
                makespan=resultado_detalhado.get('makespan', custo),
                penalidade_total=resultado_detalhado.get('penalidade', 0),
                tempo_execucao=tempo_execucao,
                solucao_json={
                    "solucao": solucao,
                    "resultado_detalhado": resultado_detalhado
                },
                parametros_json={
                    "max_iter": max_iter,
                    "objetivo": objetivo,
                    "num_maquinas": num_maquinas
                }
            )
            agendamento_id = agendamento.id
        except Exception as e:
            print(f"Erro ao salvar agendamento: {e}")
            agendamento_id = None
        
        # 6️⃣ Preparar resposta
        resposta = {
            "metodo": metodo,
            "objetivo": objetivo,
            "solucao": solucao,
            "custo_total": custo,
            "resultado_detalhado": resultado_detalhado,
            "estatisticas": {
                "tempo_execucao_segundos": round(tempo_execucao, 3),
                "num_tarefas": len(solucao),
                "num_maquinas": num_maquinas,
                "tempos_por_maquina": tempos_maquinas,
                "makespan": max(tempos_maquinas) if tempos_maquinas else custo,
                "utilizacao_media": round(sum(tempos_maquinas) / (num_maquinas * max(tempos_maquinas)), 3) if tempos_maquinas and max(tempos_maquinas) > 0 else 0
            },
            "agendamento_id": agendamento_id
        }
        
        return Response(resposta, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"erro": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
@permission_classes([AllowAny])
def agendamentos_list(request):
    """
    Lista todos os agendamentos realizados
    """
    try:
        agendamentos = Agendamento.objects.all().order_by('-created_at')[:50]  # Últimos 50
        dados = []
        
        for ag in agendamentos:
            dados.append({
                "id": ag.id,
                "nome": ag.nome,
                "algoritmo": ag.algoritmo,
                "num_maquinas": ag.num_maquinas,
                "makespan": ag.makespan,
                "penalidade_total": ag.penalidade_total,
                "tempo_execucao": ag.tempo_execucao,
                "executado_em": ag.executado_em,
                "created_at": ag.created_at
            })
        
        return Response({
            "count": len(dados),
            "agendamentos": dados
        })
        
    except Exception as e:
        return Response(
            {"erro": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
@permission_classes([AllowAny])
def agendamento_detail(request, pk):
    """
    Detalhes de um agendamento específico
    """
    try:
        agendamento = Agendamento.objects.get(pk=pk)
        
        return Response({
            "id": agendamento.id,
            "nome": agendamento.nome,
            "algoritmo": agendamento.algoritmo,
            "num_maquinas": agendamento.num_maquinas,
            "makespan": agendamento.makespan,
            "penalidade_total": agendamento.penalidade_total,
            "tempo_execucao": agendamento.tempo_execucao,
            "solucao_json": agendamento.solucao_json,
            "parametros_json": agendamento.parametros_json,
            "executado_em": agendamento.executado_em,
            "created_at": agendamento.created_at
        })
        
    except Agendamento.DoesNotExist:
        return Response(
            {"erro": "Agendamento não encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"erro": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
@permission_classes([AllowAny])
def api_docs(request):
    """
    Documentação da API
    """
    docs = {
        "endpoints": {
            "GET /api/tarefas/": "Lista todas as tarefas",
            "POST /api/tarefas/": "Cria uma nova tarefa",
            "POST /api/optimize/": "Otimiza agendamento de tarefas",
            "GET /api/agendamentos/": "Lista agendamentos realizados",
            "GET /api/agendamentos/<id>/": "Detalhes de um agendamento",
            "POST /api/token/": "Obter token JWT",
            "POST /api/token/refresh/": "Atualizar token JWT",
            "GET /dashboard/": "Interface web do sistema",
            "GET /": "Página inicial",
            "GET /api/docs/": "Esta documentação"
        },
        "autenticacao": {
            "tipo": "JWT (JSON Web Token)",
            "obter_token": "POST /api/token/ com {username, password}",
            "usar_token": "Header: Authorization: Bearer <token>"
        },
        "exemplo_optimize": {
            "method": "POST",
            "url": "/api/optimize/",
            "body": {
                "method": "sa",  # ou "busca"
                "tarefas": [
                    {"id": "T1", "nome": "Tarefa 1", "duracao": 5, "deadline": 10},
                    {"id": "T2", "nome": "Tarefa 2", "duracao": 3, "deadline": 8}
                ],
                "num_maquinas": 3,
                "max_iter": 1000,
                "objetivo": "tempo"  # ou "penalidade"
            }
        }
    }
    
    return Response(docs)

@api_view(["GET"])
@permission_classes([AllowAny])
def tarefas_exemplo(request):
    """
    Retorna um conjunto de tarefas de exemplo para testes
    """
    exemplo_tarefas = [
        {"id": "A", "nome": "Montagem Inicial", "duracao": 4, "deadline": 12, "prioridade": 3},
        {"id": "B", "nome": "Teste de Qualidade", "duracao": 2, "deadline": 5, "prioridade": 2},
        {"id": "C", "nome": "Pintura", "duracao": 6, "deadline": 18, "prioridade": 1},
        {"id": "D", "nome": "Embalagem", "duracao": 3, "deadline": 10, "prioridade": 2},
        {"id": "E", "nome": "Controle Final", "duracao": 5, "deadline": 20, "prioridade": 3},
        {"id": "F", "nome": "Logística", "duracao": 2, "deadline": 7, "prioridade": 1},
        {"id": "G", "nome": "Produção Peça A", "duracao": 7, "deadline": 15, "prioridade": 3},
        {"id": "H", "nome": "Produção Peça B", "duracao": 4, "deadline": 12, "prioridade": 2},
        {"id": "I", "nome": "Montagem Final", "duracao": 8, "deadline": 25, "prioridade": 3},
        {"id": "J", "nome": "Inspeção", "duracao": 3, "deadline": 9, "prioridade": 1}
    ]
    
    return Response(exemplo_tarefas)

@api_view(["GET"])
@permission_classes([AllowAny])
def home(request):
    """
    Página inicial do ScheduleAI
    """
    return render(request, 'scheduling/home.html')

@api_view(["GET"])
@permission_classes([AllowAny])
def dashboard(request):
    """
    Dashboard do ScheduleAI
    """
    return render(request, 'scheduling/dashboard.html')