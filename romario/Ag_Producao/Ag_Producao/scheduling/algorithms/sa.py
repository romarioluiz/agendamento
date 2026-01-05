import random
import math
from .busca import custo_multi_maquina, gerar_vizinho

def simulated_annealing(tarefas, temp_inicial=1000, temp_min=1, alpha=0.95, 
                       max_iter=100, num_maquinas=3, objetivo='tempo'):
    """
    Simulated Annealing para agendamento de produção
    
    Args:
        tarefas: Lista de tarefas
        temp_inicial: Temperatura inicial
        temp_min: Temperatura mínima
        alpha: Taxa de resfriamento
        max_iter: Iterações por temperatura
        num_maquinas: Número de máquinas
        objetivo: 'tempo' para minimizar makespan, 'penalidade' para minimizar atrasos
    """
    
    # Função de custo baseada no objetivo
    def calcular_custo(solucao):
        resultado = custo_multi_maquina(solucao, num_maquinas)
        if objetivo == 'tempo':
            return resultado['makespan']
        else:  # 'penalidade'
            return resultado['penalidade']
    
    # Solução inicial (aleatória)
    atual = tarefas.copy()
    random.shuffle(atual)
    melhor = atual.copy()
    
    custo_melhor = calcular_custo(melhor)
    temperatura = temp_inicial
    
    historico = {
        'temperaturas': [],
        'custos': [],
        'melhores_custos': []
    }
    
    while temperatura > temp_min:
        custos_iteracao = []
        
        for _ in range(max_iter):
            vizinho = gerar_vizinho(atual)
            custo_atual = calcular_custo(atual)
            custo_vizinho = calcular_custo(vizinho)
            
            delta = custo_vizinho - custo_atual
            
            if delta < 0:
                atual = vizinho
                if custo_vizinho < custo_melhor:
                    melhor = vizinho.copy()
                    custo_melhor = custo_vizinho
            else:
                prob = math.exp(-delta / temperatura)
                if random.random() < prob:
                    atual = vizinho
            
            custos_iteracao.append(custo_atual)
        
        # Registrar histórico
        historico['temperaturas'].append(temperatura)
        historico['custos'].append(sum(custos_iteracao) / len(custos_iteracao))
        historico['melhores_custos'].append(custo_melhor)
        
        # Resfriar
        temperatura *= alpha
    
    # Resultado completo
    resultado_final = custo_multi_maquina(melhor, num_maquinas)
    
    return {
        'solucao': melhor,
        'custo': custo_melhor,
        'resultado_detalhado': resultado_final,
        'historico': historico,
        'parametros': {
            'algoritmo': 'simulated_annealing',
            'temperatura_inicial': temp_inicial,
            'temperatura_minima': temp_min,
            'alpha': alpha,
            'max_iter': max_iter,
            'num_maquinas': num_maquinas,
            'objetivo': objetivo
        }
    }

if __name__ == "__main__":
    tarefas = [
        {"id": "A", "tempo": 4, "deadline": 12},
        {"id": "B", "tempo": 2, "deadline": 5},
        {"id": "C", "tempo": 6, "deadline": 18},
        {"id": "D", "tempo": 3, "deadline": 10},
        {"id": "E", "tempo": 5, "deadline": 20},
        {"id": "F", "tempo": 2, "deadline": 7}
    ]
    
    resultado = simulated_annealing(
        tarefas,
        temp_inicial=1000,
        temp_min=0.1,
        alpha=0.90,
        max_iter=200,
        num_maquinas=3,
        objetivo='tempo'
    )
    
    print("Solução encontrada:")
    print([t['id'] for t in resultado['solucao']])
    print("Makespan:", resultado['resultado_detalhado']['makespan'])
    print("Penalidade:", resultado['resultado_detalhado']['penalidade'])
    print("Custo total:", resultado['resultado_detalhado']['custo_total'])