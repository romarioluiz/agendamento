ScheduleAI — Sistema Web Inteligente para Agendamento de Produção

Descrição Geral
O ScheduleAI é um sistema web desenvolvido em Python + Django para resolver o problema de Escalonamento de Tarefas (Job Scheduling),
um problema NP-Difícil, utilizando heurísticas e metaheurísticas.

Objetivo
Minimizar o atraso total das tarefas de produção, organizando a melhor ordem de execução.

O que o código faz
- Recebe uma lista de tarefas com tempo e deadline
- Aplica Busca Local ou Simulated Annealing
- Calcula o atraso total
- Retorna a melhor sequência encontrada via API REST

Exemplo de JSON de entrada

{
  "method": "sa",
  "tarefas": [
    { "id": "A", "tempo": 4, "deadline": 12 },
    { "id": "B", "tempo": 2, "deadline": 5 },
    { "id": "C", "tempo": 6, "deadline": 18 }
  ]
}

Como testar
1. Inicie o servidor: python manage.py runserver
2. Envie o JSON para /api/optimize/
3. O sistema retorna a ordem otimizada e o atraso total
