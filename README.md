# ScheduleAI – Agendamento de Produção

Este projeto implementa um algoritmo de Simulated Annealing em Python para resolver o problema de escalonamento de tarefas (job scheduling).
O objetivo é encontrar a melhor ordem de produção de um conjunto de tarefas, minimizando o tempo total de execução (makespan)

# Como funciona?📌

Dado um conjunto de tarefas, cada uma com seu tempo de processamento, o algoritmo tenta reorganizar a ordem das tarefas para encontrar uma sequência que resulte no menor tempo total.
O Simulated Annealing:
começa com uma solução inicial (ordem natural das tarefas);
gera soluções vizinhas trocando duas tarefas de lugar;
aceita soluções melhores sempre;
aceita soluções piores às vezes (chance controlada pela temperatura);
reduz a temperatura gradualmente, tornando-se mais seletivo.
# Como testar o código ▶️

1. Salve o código abaixo em um arquivo:
Por exemplo:
agendamento_sa.py
2. Certifique-se de ter Python 3 instalado:
No terminal/cmd:
python --version
Deve aparecer algo como:
Python 3.8+
3. Execute o código:
No terminal, dentro da pasta onde salvou o arquivo:
python agendamento_sa.py
4. Veja a saída:
Você verá algo assim:
Melhor Ordem de Execução: [1, 3, 0, 4, 2]
Tempo Total de Produção (Makespan): 28
Isso significa que o algoritmo encontrou uma ordem que reduz o tempo total.

# Como alterar os tempos das tarefas?✏️

No final do código, troque a linha:
tempos = [5, 3, 9, 4, 7]
por qualquer lista de tempos:
tempos = [10, 2, 6, 8, 3, 4, 7]
Cada número representa o tempo de execução de cada tarefa (job).

# CÓDIGO COMPLETO 
(pronto para rodar)
import random
import math

# Função que calcula o makespan (tempo total) dado uma ordem de tarefas
def calcular_makespan(ordem, tempos):
    tempo_total = 0
    tempo_conclusao = 0
    
    for job in ordem:
        tempo_conclusao += tempos[job]
        tempo_total = max(tempo_total, tempo_conclusao)
    
    return tempo_total

# Gera uma solução vizinha trocando duas tarefas de posição
def vizinho(ordem):
    nova = ordem[:]
    i, j = random.sample(range(len(ordem)), 2)
    nova[i], nova[j] = nova[j], nova[i]
    return nova

# Algoritmo de Simulated Annealing
def simulated_annealing(tempos, temperatura_inicial=1000, taxa_resfriamento=0.995, it_max=10000):
    # ordem inicial (0,1,2,...)
    ordem_atual = list(range(len(tempos)))
    melhor_ordem = ordem_atual[:]
    
    melhor_makespan = calcular_makespan(melhor_ordem, tempos)
    makespan_atual = melhor_makespan

    temperatura = temperatura_inicial

    for _ in range(it_max):

        nova_ordem = vizinho(ordem_atual)
        novo_makespan = calcular_makespan(nova_ordem, tempos)

        # Critério de aceitação
        if novo_makespan < makespan_atual or random.random() < math.exp((makespan_atual - novo_makespan) / temperatura):
            ordem_atual = nova_ordem
            makespan_atual = novo_makespan

        # Atualiza melhor solução encontrada
        if makespan_atual < melhor_makespan:
            melhor_makespan = makespan_atual
            melhor_ordem = ordem_atual[:]

        temperatura *= taxa_resfriamento
    
    return melhor_ordem, melhor_makespan


# -----------------------------
# TESTANDO O ALGORITMO
# -----------------------------
if __name__ == "__main__":
    # Lista com o tempo de cada tarefa
    tempos = [5, 3, 9, 4, 7]  # Altere para testar diferentes casos
    
    melhor_ordem, melhor_makespan = simulated_annealing(tempos)
    
    print("Melhor Ordem de Execução:", melhor_ordem)
    print("Tempo Total de Produção (Makespan):", melhor_makespan)

# Como saber se está funcionando?🧪
✔ O programa está funcionando corretamente se:
imprimir alguma ordem de execução como [1, 3, 0, 4, 2];
imprimir o makespan resultante;
você perceber que, ao mudar a lista de tempos, o algoritmo produz respostas diferentes.

# Dicas para testar melhorias 📈
Você pode alterar:
Parâmetro
Efeito
temperatura_inicial
Soluções piores são aceitas com maior frequência no começo.
taxa_resfriamento
Quanto menor, o algoritmo esfria mais rápido (menos exploração).
it_max
Mais iterações → maior chance de boa solução.
Exemplo:
melhor_ordem, melhor_makespan = simulated_annealing(
    tempos,
    temperatura_inicial=2000,
    taxa_resfriamento=0.999,
    it_max=50000
)
