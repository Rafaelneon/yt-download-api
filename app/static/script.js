const API_BASE = '/youtube';

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(btn => btn.classList.remove('active'));

    document.getElementById(tabName).classList.add('active');
    const activeBtn = Array.from(document.querySelectorAll('.tab')).find(btn =>
        btn.textContent.toLowerCase().includes(tabName)
    );
    if (activeBtn) activeBtn.classList.add('active');

    if (tabName === 'queue') loadQueue();
}

async function loadQueue() {
    const queueList = document.getElementById('queueList');
    const refreshBtnText = document.getElementById('refreshBtnText');
    const refreshBtnLoading = document.getElementById('refreshBtnLoading');

    refreshBtnText.style.display = 'none';
    refreshBtnLoading.style.display = 'inline-block';

    try {
        const res = await fetch(`${API_BASE}/queue`);
        if (!res.ok) throw new Error('Erro ao carregar fila');

        const data = await res.json();

        const stats = {
            total: data.length,
            pending: data.filter(item => !item.status || item.status === 'pending').length,
            in_progress: data.filter(item => item.status === 'in_progress').length,
            completed: data.filter(item => item.status === 'completed').length,
            failed: data.filter(item => item.status === 'failed').length
        };

        updateStats(stats.total, stats.in_progress, stats.completed, stats.failed);

        if (data.length === 0) {
            queueList.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">A fila está vazia.</p>';
            return;
        }

        queueList.innerHTML = data.map(item => {
            const status = item.status || 'pending';
            const statusClass = getStatusClass(status);
            const statusText = getStatusText(status);

            return `
                <div class="queue-item">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>${item.url}</strong>
                            <span class="status-badge ${statusClass}">${statusText}</span>
                        </div>
                        <div style="color: var(--text-secondary); font-size: 14px;">
                            Tipo: ${item.type_ || item.type}
                        </div>
                    </div>
                    ${status === 'in_progress' ? `
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${item.progress || Math.random() * 40 + 60}%"></div>
                        </div>
                    ` : ''}
                    ${status === 'completed' && item.result ? `
                        <div style="margin-top: 10px; padding: 10px; background: var(--bg-tertiary); border-radius: 5px;">
                            <strong>Arquivo:</strong> ${item.result.filename || 'N/A'}<br>
                            <strong>Caminho:</strong> ${item.result.path || 'N/A'}
                        </div>
                    ` : ''}
                    ${status === 'failed' ? `
                        <div style="margin-top: 10px; padding: 10px; background: rgba(255, 68, 68, 0.1); border-radius: 5px; color: var(--error);">
                            <strong>Erro:</strong> ${item.result?.error || 'Erro desconhecido'}
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error(error);
        queueList.innerHTML = '<p style="text-align: center; color: var(--error);">Erro ao carregar fila</p>';
    } finally {
        refreshBtnText.style.display = 'inline';
        refreshBtnLoading.style.display = 'none';
    }
}

async function checkStatus() {
    const url = document.getElementById('status-url').value;
    if (!url) return showNotification('Insira uma URL', 'warning');

    try {
        const res = await fetch(`${API_BASE}/status?url=${encodeURIComponent(url)}`);
        if (res.status === 404) return showNotification('URL não encontrada na fila', 'warning');

        const data = await res.json();
        const result = `Status: ${getStatusText(data.status)}\nURL: ${data.url}\nTipo: ${data.type_ || data.type}`;
        document.getElementById('status-result').textContent = result;
    } catch {
        showNotification('Erro ao verificar status', 'error');
    }
}

async function addDownloads() {
    const groups = document.querySelectorAll('.url-input-group');
    const downloads = [];

    groups.forEach(group => {
        const url = group.querySelector('.url-input').value.trim();
        const type = group.querySelector('.type-select').value;
        if (url) downloads.push({ url, type });
    });

    if (downloads.length === 0) return showNotification('Adicione pelo menos uma URL', 'warning');

    const btn = document.querySelector('.btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="loading"></span> Processando...';
    btn.disabled = true;

    let success = 0, error = 0;

    for (const d of downloads) {
        try {
            const res = await fetch(`${API_BASE}/download?url=${encodeURIComponent(d.url)}&type_=${d.type}`, { method: 'POST' });
            if (res.ok) success++; else error++;
        } catch {
            error++;
        }
        await new Promise(r => setTimeout(r, 500));
    }

    btn.innerHTML = originalText;
    btn.disabled = false;

    if (success > 0) {
        showNotification(`${success} download(s) adicionado(s)!`, 'success');
        clearInputs();
        if (document.getElementById('queue').classList.contains('active')) loadQueue();
    }
    if (error > 0) showNotification(`${error} erro(s)`, 'error');
}

function getStatusClass(status) {
    const map = {
        pending: 'status-pending',
        in_progress: 'status-in_progress',
        completed: 'status-completed',
        failed: 'status-failed'
    };
    return map[status] || 'status-pending';
}

function getStatusText(status) {
    const map = {
        pending: 'Pendente',
        in_progress: 'Baixando',
        completed: 'Concluído',
        failed: 'Erro'
    };
    return map[status] || status;
}

async function updateStats() {
    try {
        const response = await fetch("/youtube/queue");
        const data = await response.json();

        let total = data.length;
        let active = 0;
        let completed = 0;
        let errors = 0;

        data.forEach(item => {
            switch (item.status) {
                case "IN_PROGRESS":
                    active++;
                    break;
                case "COMPLETED":
                    completed++;
                    break;
                case "FAILED":
                    errors++;
                    break;
            }
        });

        document.getElementById("totalDownloads").textContent = total;
        document.getElementById("activeDownloads").textContent = active;
        document.getElementById("completedDownloads").textContent = completed;
        document.getElementById("errorDownloads").textContent = errors;

    } catch (e) {
        console.error("Erro ao atualizar estatísticas:", e);
    }
}

// Atualiza a cada 1.5 segundos
setInterval(updateStats, 1500);

// Executa a primeira atualização ao carregar a página
updateStats();

function showNotification(message, type = 'success') {
    document.querySelectorAll('.notification').forEach(n => n.remove());
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    const colors = {
        success: '#00ff88',
        error: '#ff4444',
        warning: '#ffaa00'
    };
    notification.style.background = colors[type] || colors.success;
    if (type === 'success' || type === 'warning') notification.style.color = '#0a0a0a';

    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 4000);
}

function clearInputs() {
    document.querySelectorAll('.url-input').forEach(input => input.value = '');
    const groups = document.querySelectorAll('.url-input-group');
    for (let i = 1; i < groups.length; i++) groups[i].remove();
    if (groups[0]) groups[0].querySelector('.remove-url').style.display = 'none';
}

function addUrlInput() {
    const container = document.getElementById('urlInputs');
    const div = document.createElement('div');
    div.className = 'url-input-group';
    div.innerHTML = `
        <input type="url" placeholder="https://..." class="url-input" />
        <select class="type-select">
            <option value="video">Vídeo</option>
            <option value="music">Música</option>
        </select>
        <button class="remove-url" onclick="removeUrlInput(this)">×</button>
    `;
    container.appendChild(div);
    document.querySelectorAll('.remove-url').forEach(btn => btn.style.display = 'block');
}

function removeUrlInput(btn) {
    btn.parentElement.remove();
    const groups = document.querySelectorAll('.url-input-group');
    if (groups.length === 1) groups[0].querySelector('.remove-url').style.display = 'none';
}

// Templates
let templates = JSON.parse(localStorage.getItem('templates') || '[]');

function loadTemplates() {
    const list = document.getElementById('templateList');
    if (templates.length === 0) {
        list.innerHTML = '<p style="color: var(--text-secondary);">Nenhum template salvo.</p>';
    } else {
        list.innerHTML = templates.map((t, i) => `
            <div class="template-item" onclick="loadTemplate(${i})">
                <strong>${t.name}</strong>
                <div style="color: var(--text-secondary); font-size: 14px;">
                    ${t.urls.length} URLs • Tipo: ${t.type}
                </div>
            </div>
        `).join('');
    }
}

function saveTemplate() {
    const groups = document.querySelectorAll('.url-input-group');
    const urls = [];
    let type = 'video';
    groups.forEach(g => {
        const url = g.querySelector('.url-input').value.trim();
        if (url) {
            urls.push(url);
            type = g.querySelector('.type-select').value;
        }
    });

    if (urls.length === 0) return showNotification('Adicione pelo menos uma URL', 'warning');

    const name = prompt('Nome do template:');
    if (!name) return;

    templates.push({ name, urls, type, date: new Date().toISOString() });
    localStorage.setItem('templates', JSON.stringify(templates));
    showNotification('Template salvo!', 'success');
    loadTemplates();
}

function createTemplate() {
    const name = document.getElementById('templateName').value.trim();
    const urlsText = document.getElementById('templateUrls').value.trim();
    const type = document.getElementById('templateType').value;

    if (!name || !urlsText) return showNotification('Preencha todos os campos', 'warning');

    const urls = urlsText.split('\n').filter(u => u.trim());
    templates.push({ name, urls, type, date: new Date().toISOString() });
    localStorage.setItem('templates', JSON.stringify(templates));

    document.getElementById('templateName').value = '';
    document.getElementById('templateUrls').value = '';

    showNotification('Template criado!', 'success');
    loadTemplates();
}

function loadTemplate(index) {
    const t = templates[index];
    clearInputs();
    t.urls.forEach((url, i) => {
        if (i > 0) addUrlInput();
        const groups = document.querySelectorAll('.url-input-group');
        groups[i].querySelector('.url-input').value = url;
        groups[i].querySelector('.type-select').value = t.type;
    });
    showTab('downloads');
    showNotification(`Template "${t.name}" carregado!`, 'success');
}

// Configurações
function saveSettings() {
    localStorage.setItem('apiUrl', document.getElementById('apiUrl').value);
    localStorage.setItem('refreshInterval', document.getElementById('refreshInterval').value);
    localStorage.setItem('autoRefresh', document.getElementById('autoRefresh').checked);
    showNotification('Configurações salvas!', 'success');
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    showTab('downloads');
    setInterval(() => {
        if (document.getElementById('queue').classList.contains('active')) loadQueue();
    }, 2000);
});