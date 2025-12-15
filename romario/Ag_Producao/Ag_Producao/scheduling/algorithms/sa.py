import random
import math
##reaproveitando o arquivo busca para limpar o codigo
from .busca import custo, gerar_vizinho, solucao_inicial

def simulated_annealing(tarefas, temp_inicial=1000, temp_min=1, alpha=0.95, max_iter=100):
    atual = solucao_inicial(tarefas)
    melhor = atual
    temperatura = temp_inicial

    while temperatura > temp_min:
        for _ in range(max_iter):
            vizinho = gerar_vizinho(atual)

            delta = custo(vizinho) - custo(atual)

            if delta < 0:
                atual = vizinho
            else:
                prob = math.exp(-delta / temperatura)
                if random.random() < prob:
                    atual = vizinho

            if custo(atual) < custo(melhor):
                melhor = atual

        temperatura *= alpha

    return melhor, custo(melhor)



if __name__ == "__main__":
    tarefas = [
    {"id": "A", "tempo": 4, "deadline": 12},
    {"id": "B", "tempo": 2, "deadline": 5},
    {"id": "C", "tempo": 6, "deadline": 18},
    {"id": "D", "tempo": 3, "deadline": 10},
    {"id": "E", "tempo": 5, "deadline": 20},
    {"id": "F", "tempo": 2, "deadline": 7}
    ]

    solucao, custo_final = simulated_annealing(
        tarefas,
        temp_inicial=1000,
        temp_min=0.1,
        alpha=0.90,
        max_iter=200

        )
    
    print(solucao)
    print("Atraso total:", custo_final)