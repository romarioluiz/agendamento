# 🏭 Ag_Producao - Sistema Inteligente de Agendamento de Produção

> **Sistema web completo para otimização de tarefas em ambientes de produção utilizando algoritmos de Inteligência Artificial**

## 🚀 Começando

### 📋 Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Git (para controle de versão)

### 🔧 Instalação Rápida (3 minutos)

```bash
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