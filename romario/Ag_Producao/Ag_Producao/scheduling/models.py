from django.db import models

class TarefaProducao(models.Model):
    nome = models.CharField(max_length=100)
    duracao = models.IntegerField(help_text="Duração em minutos")
    prioridade = models.IntegerField(default=1)

    def __str__(self):
        return self.nome
