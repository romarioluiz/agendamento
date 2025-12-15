def custo(solucao):
    tempo_atual = 0
    penalidade = 0

    for tarefa in solucao:
        tempo_atual += tarefa["tempo"]

        if tempo_atual > tarefa["deadline"]:
            penalidade += tempo_atual - tarefa["deadline"]

    return penalidade
def solucao_inicial(tarefas):
    return tarefas.copy()
##geramos o visinho que é excencia da busca local
import random
## trocamos 2 tarefas de lugar o que gera o movimento local
def gerar_vizinho(solucao):
    vizinho = solucao.copy()
    i, j = random.sample(range(len(vizinho)), 2)
    vizinho[i], vizinho[j]= vizinho[j], vizinho[i]
    return vizinho
def busca_local(tarefas, max_iter=1000):
    atual = solucao_inicial(tarefas)
    melhor = atual

    for _ in range(max_iter):
        vizinho = gerar_vizinho(atual)

        if custo(vizinho) < custo(melhor):
            melhor = vizinho
            atual = vizinho

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

    solucao, custo_final = busca_local(tarefas)
    print(solucao)
    print("Atraso total:", custo_final)