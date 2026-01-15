# 🧪 Testes para Outros Grupos

## Instância Pequena (Teste Rápido)
```
{
  "grupo_tester": "[NOME_GRUPO]",
  "method": "sa",
  "tarefas": [
    {"id": "T1", "duracao": 4, "deadline": 10},
    {"id": "T2", "duracao": 3, "deadline": 8}
  ],
  "num_maquinas": 2,
  "max_iter": 100
}
```
## Instância Média (Performance) 

```

{
  "grupo_tester": "GRUPO_EXEMPLO",
  "method": "sa",
  "tarefas": [
    { "id": "T1", "duracao": 3, "deadline": 10 },
    { "id": "T2", "duracao": 5, "deadline": 14 },
    { "id": "T3", "duracao": 2, "deadline": 8 },
    { "id": "T4", "duracao": 6, "deadline": 18 },
    { "id": "T5", "duracao": 4, "deadline": 12 },
    { "id": "T6", "duracao": 3, "deadline": 11 }
  ],
  "num_maquinas": 3,
  "max_iter": 500
}

```
## Instância Complexa (Estresse)

```{
  "grupo_tester": "GRUPO_EXEMPLO",
  "method": "sa",
  "tarefas": [
    { "id": "T1",  "duracao": 4, "deadline": 12 },
    { "id": "T2",  "duracao": 6, "deadline": 15 },
    { "id": "T3",  "duracao": 3, "deadline": 9 },
    { "id": "T4",  "duracao": 7, "deadline": 20 },
    { "id": "T5",  "duracao": 5, "deadline": 14 },
    { "id": "T6",  "duracao": 8, "deadline": 22 },
    { "id": "T7",  "duracao": 2, "deadline": 8 },
    { "id": "T8",  "duracao": 6, "deadline": 16 },
    { "id": "T9",  "duracao": 4, "deadline": 13 },
    { "id": "T10", "duracao": 5, "deadline": 17 },
    { "id": "T11", "duracao": 9, "deadline": 25 },
    { "id": "T12", "duracao": 3, "deadline": 11 }
  ],
  "num_maquinas": 4,
  "max_iter": 1000
}

```
## O que Avaliar

1. ✅ API responde? (GET /api/health/)

2. ✅ Tempo < 3 segundos?

3. ✅ Makespan razoável?

4. ✅ Balanceamento > 0.5?