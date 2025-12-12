from django.db import models

class TarefaProducao(models.Model):
    nome_produto = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    tempo_estimado = models.FloatField(help_text="Tempo estimado em horas")
    prioridade = models.IntegerField(default=1)  # 1 = alta, 2 = baixa

    def __str__(self):
        return f"{self.nome_produto} - {self.quantidade}"
