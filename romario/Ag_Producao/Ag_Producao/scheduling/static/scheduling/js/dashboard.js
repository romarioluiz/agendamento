// Variáveis globais
let tarefasAtuais = [];
let resultadoAtual = null;

// Função para mostrar seções
function showSection(sectionId) {
    // Esconder todas as seções
    document.querySelectorAll('[id^="section-"]').forEach(el => {
        el.classList.add('d-none');
    });
    
    // Remover classe active de todos os links
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Mostrar seção selecionada
    document.getElementById(`section-${sectionId}`).classList.remove('d-none');
    
    // Ativar link correspondente
    document.querySelector(`.sidebar .nav-link[onclick*="${sectionId}"]`).classList.add('active');
    
    // Carregar dados se necessário
    if (sectionId === 'historico') {
        carregarHistorico();
    } else if (sectionId === 'tarefas') {
        carregarTarefasDoBanco();
    } else if (sectionId === 'estatisticas') {
        carregarEstatisticas();
    }
}

// Carregar tarefas de exemplo
async function carregarTarefasExemplo() {
    try {
        const response = await fetch('/api/tarefas/exemplo/');
        if (!response.ok) throw new Error('Erro ao carregar tarefas');
        
        tarefasAtuais = await response.json();
        atualizarListaTarefas();
        
        // Mostrar mensagem de sucesso
        alert('✅ Tarefas de exemplo carregadas com sucesso!');
    } catch (error) {
        console.error('Erro:', error);
        alert('❌ Erro ao carregar tarefas de exemplo');
    }
}

// Atualizar lista visual de tarefas
function atualizarListaTarefas() {
    const container = document.getElementById('tarefas-lista');
    if (!container) return;
    
    if (tarefasAtuais.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                Nenhuma tarefa adicionada. Clique em "Carregar Tarefas de Exemplo" ou "Adicionar Tarefa".
            </div>
        `;
        return;
    }
    
    let html = '<div class="table-responsive"><table class="table table-sm">';
    html += '<thead><tr><th>ID</th><th>Nome</th><th>Duração</th><th>Deadline</th><th>Prioridade</th><th>Ações</th></tr></thead><tbody>';
    
    tarefasAtuais.forEach((tarefa, index) => {
        html += `
            <tr>
                <td>${tarefa.id || index + 1}</td>
                <td>${tarefa.nome}</td>
                <td>${tarefa.duracao || tarefa.tempo} min</td>
                <td>${tarefa.deadline}</td>
                <td>
                    <span class="badge ${tarefa.prioridade === 3 ? 'bg-danger' : tarefa.prioridade === 2 ? 'bg-warning' : 'bg-secondary'}">
                        ${tarefa.prioridade === 3 ? 'Alta' : tarefa.prioridade === 2 ? 'Média' : 'Baixa'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-danger" onclick="removerTarefa(${index})">
                        ✕
                    </button>
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    container.innerHTML = html;
}

// Adicionar tarefa manualmente
function adicionarTarefa() {
    // Abrir modal
    const modal = new bootstrap.Modal(document.getElementById('modalTarefa'));
    modal.show();
    
    // Limpar campos
    document.getElementById('tarefa-nome').value = '';
    document.getElementById('tarefa-duracao').value = '5';
    document.getElementById('tarefa-deadline').value = '10';
    document.getElementById('tarefa-prioridade').value = '2';
}

// Salvar tarefa do modal
function salvarTarefa() {
    const nome = document.getElementById('tarefa-nome').value.trim();
    const duracao = parseInt(document.getElementById('tarefa-duracao').value);
    const deadline = parseInt(document.getElementById('tarefa-deadline').value);
    const prioridade = parseInt(document.getElementById('tarefa-prioridade').value);
    
    if (!nome || isNaN(duracao) || duracao <= 0) {
        alert('Por favor, preencha todos os campos corretamente.');
        return;
    }
    
    // Adicionar à lista
    tarefasAtuais.push({
        id: `T${tarefasAtuais.length + 1}`,
        nome: nome,
        duracao: duracao,
        tempo: duracao,
        deadline: deadline,
        prioridade: prioridade
    });
    
    atualizarListaTarefas();
    
    // Fechar modal
    bootstrap.Modal.getInstance(document.getElementById('modalTarefa')).hide();
    
    alert('✅ Tarefa adicionada com sucesso!');
}

// Remover tarefa
function removerTarefa(index) {
    if (confirm('Tem certeza que deseja remover esta tarefa?')) {
        tarefasAtuais.splice(index, 1);
        atualizarListaTarefas();
    }
}

// Executar otimização
async function executarOtimizacao() {
    if (tarefasAtuais.length === 0) {
        alert('❌ Adicione pelo menos uma tarefa antes de executar a otimização.');
        return;
    }
    
    // Mostrar loading
    const resultadosDiv = document.getElementById('resultados');
    resultadosDiv.innerHTML = `
        <div class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Processando...</span>
            </div>
            <p class="mt-2">Processando otimização com ${document.getElementById('algoritmo').value === 'sa' ? 'Simulated Annealing' : 'Busca Local'}...</p>
        </div>
    `;
    
    // Mostrar card de resultados
    document.getElementById('resultados-card').classList.remove('d-none');
    
    try {
        const dados = {
            method: document.getElementById('algoritmo').value,
            tarefas: tarefasAtuais,
            num_maquinas: parseInt(document.getElementById('num-maquinas').value),
            max_iter: parseInt(document.getElementById('max-iter').value),
            objetivo: document.getElementById('objetivo').value
        };
        
        const response = await fetch('/api/optimize/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(dados)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${await response.text()}`);
        }
        
        resultadoAtual = await response.json();
        mostrarResultados(resultadoAtual);
        
    } catch (error) {
        console.error('Erro na otimização:', error);
        resultadosDiv.innerHTML = `
            <div class="alert alert-danger">
                <h5>❌ Erro na Otimização</h5>
                <p>${error.message}</p>
                <p>Verifique os dados e tente novamente.</p>
            </div>
        `;
    }
}

// Mostrar resultados da otimização
function mostrarResultados(resultado) {
    const container = document.getElementById('resultados');
    
    // Extrair dados
    const algoritmo = resultado.metodo === 'sa' ? 'Simulated Annealing' : 'Busca Local';
    const objetivo = resultado.objetivo === 'tempo' ? 'Tempo Total' : 'Atrasos';
    const estatisticas = resultado.estatisticas || {};
    
    let html = `
        <div class="alert alert-success">
            <h4>✅ Otimização Concluída com Sucesso!</h4>
            <p><strong>Algoritmo:</strong> ${algoritmo} | <strong>Objetivo:</strong> Minimizar ${objetivo}</p>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">📊 Estatísticas</h5>
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item d-flex justify-content-between">
                                <span>Makespan:</span>
                                <strong>${estatisticas.makespan || resultado.custo_total || 0} min</strong>
                            </li>
                            <li class="list-group-item d-flex justify-content-between">
                                <span>Tempo de Execução:</span>
                                <strong>${estatisticas.tempo_execucao_segundos || 0} seg</strong>
                            </li>
                            <li class="list-group-item d-flex justify-content-between">
                                <span>Número de Tarefas:</span>
                                <strong>${estatisticas.num_tarefas || 0}</strong>
                            </li>
                            <li class="list-group-item d-flex justify-content-between">
                                <span>Número de Máquinas:</span>
                                <strong>${estatisticas.num_maquinas || 0}</strong>
                            </li>
                            <li class="list-group-item d-flex justify-content-between">
                                <span>Utilização Média:</span>
                                <strong>${(estatisticas.utilizacao_media * 100 || 0).toFixed(1)}%</strong>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">🏭 Distribuição por Máquina</h5>
    `;
    
    // Mostrar tempos por máquina
    if (estatisticas.tempos_por_maquina) {
        estatisticas.tempos_por_maquina.forEach((tempo, idx) => {
            const percentual = estatisticas.makespan ? (tempo / estatisticas.makespan * 100).toFixed(1) : 0;
            html += `
                <div class="mb-2">
                    <div class="d-flex justify-content-between mb-1">
                        <span>Máquina ${idx + 1}:</span>
                        <span>${tempo} min (${percentual}%)</span>
                    </div>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar" role="progressbar" 
                             style="width: ${percentual}%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                        </div>
                    </div>
                </div>
            `;
        });
    }
    
    html += `
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mt-3">
            <div class="card-body">
                <h5 class="card-title">📋 Sequência Otimizada</h5>
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Ordem</th>
                                <th>Tarefa</th>
                                <th>Duração</th>
                                <th>Deadline</th>
                                <th>Máquina</th>
                            </tr>
                        </thead>
                        <tbody>
    `;
    
    // Mostrar sequência de tarefas
    if (resultado.solucao && Array.isArray(resultado.solucao)) {
        resultado.solucao.forEach((tarefa, index) => {
            const maquina = (index % (estatisticas.num_maquinas || 3)) + 1;
            html += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${tarefa.nome || tarefa.id}</td>
                    <td>${tarefa.tempo || tarefa.duracao} min</td>
                    <td>${tarefa.deadline}</td>
                    <td>
                        <span class="badge bg-primary">Máquina ${maquina}</span>
                    </td>
                </tr>
            `;
        });
    }
    
    html += `
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <div class="mt-3">
            <button class="btn btn-outline-primary" onclick="visualizarGrafico()">
                📈 Visualizar Gráfico de Gantt
            </button>
            <button class="btn btn-outline-secondary ms-2" onclick="exportarResultados()">
                💾 Exportar Resultados
            </button>
        </div>
    `;
    
    container.innerHTML = html;
}

// Funções auxiliares
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function carregarHistorico() {
    // Implementar carregamento do histórico
    document.getElementById('historico-container').innerHTML = `
        <div class="alert alert-info">
            Funcionalidade de histórico em desenvolvimento.
        </div>
    `;
}

function carregarTarefasDoBanco() {
    // Implementar carregamento de tarefas do banco
    document.getElementById('tarefas-container').innerHTML = `
        <div class="alert alert-info">
            Funcionalidade de gerenciamento de tarefas em desenvolvimento.
        </div>
    `;
}

function carregarEstatisticas() {
    // Implementar estatísticas
    document.getElementById('chart-agendamentos').innerHTML = '<p>Gráfico em desenvolvimento</p>';
    document.getElementById('chart-tempos').innerHTML = '<p>Gráfico em desenvolvimento</p>';
}

function visualizarGrafico() {
    alert('Funcionalidade de gráfico Gantt em desenvolvimento.');
}

function exportarResultados() {
    if (!resultadoAtual) {
        alert('Nenhum resultado para exportar.');
        return;
    }
    
    const dados = JSON.stringify(resultadoAtual, null, 2);
    const blob = new Blob([dados], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `scheduleai-resultado-${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Atualizar hora atual
function atualizarHora() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('pt-BR');
    const dateString = now.toLocaleDateString('pt-BR');
    const element = document.getElementById('current-time');
    if (element) {
        element.textContent = `${dateString} ${timeString}`;
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Atualizar hora a cada segundo
    setInterval(atualizarHora, 1000);
    atualizarHora();
    
    // Carregar tarefas de exemplo automaticamente
    carregarTarefasExemplo();
    
    // Mostrar seção inicial
    showSection('optimize');
});