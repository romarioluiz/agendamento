# 📐 Especificação do Sistema

## Problema
Agendamento de tarefas em múltiplas máquinas para minimizar tempo total (makespan) e atrasos.

## Modelo Matemático
**Minimizar:** makespan + 0.5 × Σ atrasos

**Restrições:**
1. Cada máquina processa uma tarefa por vez
2. Tarefas não podem ser interrompidas
3. Penalizamos atrasos, mas não proibimos

## Arquitetura
Dashboard → API Django → Algoritmos (SA/Busca) → SQLite