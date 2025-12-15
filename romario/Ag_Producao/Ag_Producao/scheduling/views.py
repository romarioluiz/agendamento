##
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .algorithms.busca import busca_local
from .algorithms.sa import simulated_annealing

@api_view(["POST"])
def optimize(request):
    """
    Endpoint responsável por otimizar o escalonamento de tarefas
    usando Busca Local ou Simulated Annealing.
    """

    # 1️⃣ Lê o JSON enviado
    metodo = request.data.get("method", "busca")
    tarefas = request.data.get("tarefas", [])

    # 2️⃣ Validação simples
    if not tarefas:
        return Response(
            {"erro": "Lista de tarefas vazia ou não enviada"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 3️⃣ Escolhe o algoritmo
    if metodo == "sa":
        solucao, custo = simulated_annealing(tarefas)
    elif metodo == "busca":
        solucao, custo = busca_local(tarefas)
    else:
        return Response(
            {"erro": "Método inválido. Use 'busca' ou 'sa'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 4️⃣ Retorno da API
    return Response(
        {
            "metodo": metodo,
            "solucao": solucao,
            "atraso_total": custo
        },
        status=status.HTTP_200_OK
    )
