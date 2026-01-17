import random
import copy

def custo(solucao):
    tempo_atual = 0
    penalidade = 0

    for tarefa in solucao:
        tempo_atual += tarefa["tempo"]

        if tempo_atual > tarefa["deadline"]:
            penalidade += tempo_atual - tarefa["deadline"]

    return penalidade

def custo_multi_maquina(solucao, num_maquinas=3):
    """
    Calcula o custo para múltiplas máquinas (makespan + penalidade)
    """
    # Inicializa tempo para cada máquina
    tempos_maquinas = [0] * num_maquinas
    penalidade_total = 0
    
    # Distribui tarefas round-robin
    for idx, tarefa in enumerate(solucao):
        maquina = idx % num_maquinas
        tempos_maquinas[maquina] += tarefa["tempo"]
        
        # Verifica penalidade
        if tempos_maquinas[maquina] > tarefa.get("deadline", float('inf')):
            penalidade_total += tempos_maquinas[maquina] - tarefa.get("deadline", 0)
    
    # Makespan é o maior tempo entre as máquinas
    makespan = max(tempos_maquinas)
    
    return {
        'makespan': makespan,
        'penalidade': penalidade_total,
        'custo_total': makespan + penalidade_total,
        'tempos_maquinas': tempos_maquinas
    }

def solucao_inicial(tarefas):
    return tarefas.copy()

def gerar_vizinho(solucao):
    vizinho = solucao.copy()
    if len(vizinho) > 1:
        i, j = random.sample(range(len(vizinho)), 2)
        vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
    return vizinho

def busca_local(tarefas, max_iter=1000, num_maquinas=3):
    atual = solucao_inicial(tarefas)
    melhor = atual
    
    melhor_custo = custo_multi_maquina(melhor, num_maquinas)
    
    for _ in range(max_iter):
        vizinho = gerar_vizinho(atual)
        vizinho_custo = custo_multi_maquina(vizinho, num_maquinas)
        
        if vizinho_custo['custo_total'] < melhor_custo['custo_total']:
            melhor = vizinho
            melhor_custo = vizinho_custo
            atual = vizinho
        else:
            # Com pequena probabilidade, aceita solução pior (para evitar mínimos locais)
            if random.random() < 0.1:
                atual = vizinho
    
    return melhor, melhor_custo

def busca_local_tempo(tarefas, max_iter=1000, num_maquinas=3):
    """
    Versão focada apenas em minimizar o tempo total (makespan)
    """
    atual = solucao_inicial(tarefas)
    melhor = atual
    
    melhor_makespan = custo_multi_maquina(melhor, num_maquinas)['makespan']
    
    for _ in range(max_iter):
        vizinho = gerar_vizinho(atual)
        vizinho_makespan = custo_multi_maquina(vizinho, num_maquinas)['makespan']
        
        if vizinho_makespan < melhor_makespan:
            melhor = vizinho
            melhor_makespan = vizinho_makespan
            atual = vizinho
    
    return melhor, melhor_makespan

if __name__ == "__main__":
    tarefas = [
        {"id": "A", "tempo": 4, "deadline": 12},
        {"id": "B", "tempo": 2, "deadline": 5},
        {"id": "C", "tempo": 6, "deadline": 18},
        {"id": "D", "tempo": 3, "deadline": 10},
        {"id": "E", "tempo": 5, "deadline": 20},
        {"id": "F", "tempo": 2, "deadline": 7}
    ]
    
    solucao, resultado = busca_local(tarefas, num_maquinas=3)
    print("Solução encontrada:")
    print([t['id'] for t in solucao])
    print("Resultado:", resultado)