# 🏭  - Sistema Inteligente de Agendamento de Produção

> **Sistema web completo para otimização de tarefas em ambientes de produção utilizando algoritmos de Inteligência Artificial**

## 🚀 Começando

### 📋 Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Git (para controle de versão)

### 🔧 Instalação Rápida (3 minutos)

```
# 1. Clone o repositório
git clone https://gitlab.betim.ifmg.edu.br/0080031/workshop.git
cd workshop/Ag_Producao

# 2. Crie e ative um ambiente virtual (recomendado)
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o banco de dados
python manage.py migrate

# 5. Crie um superusuário (opcional)
python manage.py createsuperuser

# 6. Execute o servidor
python manage.py runserver

```


## 🌐 Acesso ao Sistema 
- Dashboard: http://localhost:8000/dashboard/
- API Health Check: http://localhost:8000/api/health/
- Documentação da API: http://localhost:8000/api/docs/

## 📊 Funcionalidades Principais

### 🎯 Otimização Inteligente

- Simulated Annealing - Algoritmo meta-heurístico para busca global

- Busca Local - Algoritmo de melhoria iterativa

- Múltiplos objetivos - Minimizar tempo total ou atrasos

- Configuração flexível - Número variável de máquinas e tarefas

### 🖥️ Interface Web
- Dashboard intuitivo para envio de tarefas

- Visualização em tempo real dos resultados

- Gráficos de distribuição por máquina

- Histórico de agendamentos executados

## 🔌 API REST Completa
Endpoint /api/optimize/ para integração

Formato JSON padronizado

Metadados para teste cruzado entre grupos

Documentação automática

## 🧪 Como Testar

### Teste Rápido (1 minuto)
1. Acesse http://localhost:8000/dashboard/

2. Clique em "Carregar Tarefas de Exemplo"

3. Clique em "Executar Otimização"

4. Veja os resultados automaticamente

### Teste via API (para outros grupos)

```
curl -X POST http://localhost:8000/api/optimize/ \
  -H "Content-Type: application/json" \
  -d '{
    "grupo_tester": "SeuGrupo",
    "method": "sa",
    "tarefas": [
      {"id": "T1", "nome": "Montagem", "duracao": 5, "deadline": 10},
      {"id": "T2", "nome": "Pintura", "duracao": 3, "deadline": 8}
    ],
    "num_maquinas": 3,
    "max_iter": 1000,
    "objetivo": "tempo"
  }'

  ```