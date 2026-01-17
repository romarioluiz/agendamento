from django.urls import path
from . import views

urlpatterns = [
    # Endpoint principal de otimização
    path("optimize/", views.optimize, name="optimize"),
    
    # Novos endpoints para o sistema completo
    path("tarefas/", views.tarefa_list, name="tarefa-list"),
    path("tarefas/exemplo/", views.tarefas_exemplo, name="tarefas-exemplo"),
    path("agendamentos/", views.agendamentos_list, name="agendamentos-list"),
    path("agendamentos/<int:pk>/", views.agendamento_detail, name="agendamento-detail"),
    
    # Dashboard e documentação
    path("dashboard/", views.dashboard, name="dashboard"),
    path("docs/", views.api_docs, name="api-docs"),
    
    # Página inicial
    path("", views.home, name="home"),
    path('health/', views.health_check, name='health-check'),

]