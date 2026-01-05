from django.db import models

class TarefaProducao(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Tarefa")
    duracao = models.IntegerField(help_text="Duração em minutos", verbose_name="Duração")
    prioridade = models.IntegerField(
        default=1, 
        choices=[(1, 'Baixa'), (2, 'Média'), (3, 'Alta')],
        verbose_name="Prioridade"
    )
    deadline = models.IntegerField(
        help_text="Prazo máximo em minutos",
        verbose_name="Prazo Máximo",
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tarefa de Produção"
        verbose_name_plural = "Tarefas de Produção"
        ordering = ['prioridade', 'nome']
    
    def __str__(self):
        return f"{self.nome} ({self.duracao} min)"

class Agendamento(models.Model):
    ALGORITMO_CHOICES = [
        ('busca_local', 'Busca Local'),
        ('simulated_annealing', 'Simulated Annealing'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome do Agendamento")
    algoritmo = models.CharField(max_length=50, choices=ALGORITMO_CHOICES)
    num_maquinas = models.IntegerField(default=3, verbose_name="Número de Máquinas")
    
    # Resultados
    solucao_json = models.JSONField(null=True, blank=True, verbose_name="Solução (JSON)")
    makespan = models.IntegerField(null=True, blank=True, verbose_name="Makespan")
    penalidade_total = models.IntegerField(null=True, blank=True, verbose_name="Penalidade Total")
    tempo_execucao = models.FloatField(null=True, blank=True, verbose_name="Tempo de Execução (s)")
    
    # Parâmetros do algoritmo
    parametros_json = models.JSONField(default=dict, verbose_name="Parâmetros do Algoritmo")
    
    created_at = models.DateTimeField(auto_now_add=True)
    executado_em = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.nome} - {self.get_algoritmo_display()}"