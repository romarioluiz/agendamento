# ⚙️ Parâmetros dos Algoritmos

## Simulated Annealing (Padrão)
- temp_inicial: 1000
- temp_min: 0.1
- alpha: 0.95 (taxa resfriamento)
- iter_por_temp: 100

## Busca Local
- max_iter: 1000
- vizinhanca: "swap" (troca tarefas)

## Objetivos
1. "tempo": Minimizar makespan
2. "penalidade": Minimizar atrasos

## Métricas Retornadas
- makespan: tempo total (menor = melhor)
- balanceamento_carga: 0-1 (1 = perfeito)
- penalidade_total: atrasos (0 = ideal)
- tempo_execucao_segundos: < 3s aceitável