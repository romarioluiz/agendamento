from django.db import models

# Classe que representa uma máquina
class Machine(models.Model):
    # Nome da máquina
    name = models.CharField(max_length=100)

    # Isso serve para mostrar o nome da máquina no admin do Django
    def __str__(self):
        return self.name


# Classe que representa uma tarefa
class Task(models.Model):
    # Nome da tarefa
    name = models.CharField(max_length=200)

    # Duração da tarefa em minutos
    # Usei PositiveIntegerField para não permitir número negativo
    duration = models.PositiveIntegerField()

    # Máquina onde a tarefa será executada
    # ForeignKey significa que uma máquina pode ter várias tarefas
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE
    )

    # Prazo final da tarefa (pode ficar vazio)
    deadline = models.DateTimeField(null=True, blank=True)

    # Mostra o nome da tarefa no admin do Django
    def __str__(self):
        return self.name
