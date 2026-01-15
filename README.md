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

  ## 🏗️ Arquitetura do Sistema


```
Frontend (Dashboard Django)
        ↓
   API REST Django
        ↓
  Algoritmos de Otimização
    ├── Simulated Annealing
    └── Busca Local
        ↓
   Banco de Dados SQLite
        ↓
   Visualização de Resultados
```


## 📁 Estrutura do Projeto
```
Ag_Producao/
├── algorithms/          # Implementação dos algoritmos
│   ├── sa.py           # Simulated Annealing
│   └── busca.py        # Busca Local
├── scheduling/         # Aplicação Django principal
│   ├── views.py        # Endpoints da API
│   ├── models.py       # Modelos de dados
│   ├── templates/      # Interface web
│   └── static/         # Arquivos estáticos
├── config/             # Configuração Django
├── docs/              # Documentação técnica
├── relatorios/        # Templates para testes
├── manage.py          # Script de administração
└── requirements.txt   # Dependências do projeto
```

## ⚙️ Parâmetros dos Algoritmos

### Simulated Annealing

| Parâmetro    | Valor Padrão | Descrição                       |
|--------------|--------------|---------------------------------|
| temp_inicial | 1000         | Temperatura inicial do SA       |
| temp_min     | 0.1          | Temperatura mínima para parada  |
| alpha        | 0.95         | Taxa de resfriamento (0.9-0.99) |
| max_iter     | 100          | Iterações por temperatura       |

### Busca Local

| Parâmetro  | Valor Padrão | Descrição                       |
|------------|--------------|---------------------------------|
| max_iter   | 1000         | Máximo de iterações             |
| vizinhanca | "swap"       | Tipo de movimento na vizinhança |


## 📈 Métricas Retornadas
A API retorna as seguintes métricas para avaliação:

| Métrica                 | Descrição                 | Ideal                |
|-------------------------|---------------------------|----------------------|
| makespan                | Tempo total de conclusão  | Quanto menor, melhor |
| balanceamento_carga     | Equilíbrio entre máquinas | Próximo de 1.0       |
| tempo_execucao_segundos | Tempo do algoritmo        | < 3 segundos         |
| penalidade_total        | Soma dos atrasos          | 0 (nenhum atraso)    |
| utilizacao_media        | % de uso das máquinas     | > 70%                |

## 🧪 Casos de Teste Padronizados

Para teste cruzado entre grupos, utilize:

1. Instância Pequena - 5 tarefas, 2 máquinas (validação funcional)

2. Instância Média - 10 tarefas, 3 máquinas (teste de performance)

3. Instância Complexa - 15 tarefas, 4 máquinas (escalabilidade)

Consulte docs/TESTES_INTERGRUPAIS.md para exemplos completos.

## 👥 Teste Cruzado entre Grupos
Para outros grupos testarem:

- Verifique se nossa API está online: GET /api/health/

- Execute casos de teste padronizados

- Avalie pelas métricas retornadas

- Preencha o template em relatorios/TEMPLATE_TESTE_CRUZADO.md

## Métricas de avaliação:

- ✅ Tempo de resposta: < 3 segundos

- ✅ Qualidade da solução: makespan competitivo

- ✅ Estabilidade: resultados consistentes

- ✅ Documentação: clara e completa

## 🐛 Solução de Problemas Comuns

### "API não responde"

```
# Verifique se o servidor está rodando
python manage.py runserver

# Teste a saúde da API
curl http://localhost:8000/api/health/

```
### "Erro 404 - Página não encontrada"

- Certifique-se de usar a porta 8000

- URL correta: http://localhost:8000/dashboard/

- Verifique se digitou /dashboard/ no final


### "Erro ao instalar dependências"

```
# Atualize o pip
pip install --upgrade pip

# Tente instalar novamente
pip install -r requirements.txt

```
 ## 📄 Licença
Este projeto foi desenvolvido para fins acadêmicos no IFMG - Campus Betim como parte da disciplina de Otimização e Inteligência Artificial.

## 👨‍🎓 Autores
- *Romário* - Desenvolvimento, algoritmos e documentação

Colegas de Grupo - Testes 

📞 Suporte
Para questões sobre o projeto:

Issues no GitLab: https://gitlab.betim.ifmg.edu.br/0080031/workshop

Contato: [seu-email]@ifmg.edu.br

🎯 Status do Projeto: ✅ PRONTO PARA TESTE CRUZADO
Última atualização: Janeiro 2026
Versão: 1.0