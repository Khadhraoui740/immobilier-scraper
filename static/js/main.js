/* JavaScript pour l'interface d'administration */

// Utilitaires
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        return await response.json();
    } catch (error) {
        console.error('Erreur API:', error);
        showNotification('Erreur: ' + error.message, 'error');
        return null;
    }
}

function showNotification(message, type = 'info') {
    const div = document.createElement('div');
    div.className = `notification notification-${type}`;
    div.textContent = message;
    document.body.appendChild(div);
    
    setTimeout(() => {
        div.style.opacity = '0';
        setTimeout(() => div.remove(), 300);
    }, 3000);
}

// Formatage
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('fr-FR');
}

// Actions principales
async function scrapeAll() {
    const button = event.target;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scraping...';
    
    const result = await apiCall('/api/scrape', 'POST', {source: 'all'});
    
    button.disabled = false;
    button.innerHTML = '<i class="fas fa-search"></i> Scraper Maintenant';
    
    if (result && result.success) {
        showNotification(`${result.new} nouvelle(s) propriété(s) trouvée(s)`, 'success');
        setTimeout(() => location.reload(), 1000);
    }
}

async function testEmail() {
    const result = await apiCall('/api/alerts/test', 'POST');
    
    if (result && result.success) {
        showNotification('Email de test envoyé avec succès', 'success');
    } else {
        showNotification('Erreur lors de l\'envoi de l\'email', 'error');
    }
}

// Fonctions de gestion de la base de données
async function optimizeDB() {
    if (!confirm('Ceci peut prendre quelques secondes...')) return;
    
    const result = await apiCall('/api/db/optimize', 'POST');
    if (result && result.success) {
        showNotification('Base de données optimisée!', 'success');
        if (typeof loadStats === 'function') {
            loadStats();
        }
    } else {
        showNotification('Erreur lors de l\'optimisation', 'error');
    }
}

async function cleanupDB() {
    if (!confirm('Ceci supprimera les doublons. Continuer?')) return;
    
    const result = await apiCall('/api/db/cleanup', 'POST');
    if (result && result.success) {
        showNotification(result.message || 'Nettoyage effectué!', 'success');
        if (typeof loadStats === 'function') {
            loadStats();
        }
    } else {
        showNotification('Erreur lors du nettoyage', 'error');
    }
}

async function resetDB() {
    if (!confirm('⚠️ ATTENTION: Ceci supprimera TOUTES les données!\n\nÊtes-vous vraiment sûr?')) return;
    
    const result = await apiCall('/api/db/reset', 'POST');
    if (result && result.success) {
        showNotification('Base de données réinitialisée!', 'success');
        setTimeout(() => location.reload(), 1000);
    } else {
        showNotification('Erreur lors de la réinitialisation', 'error');
    }
}

async function startScheduler() {
    const result = await apiCall('/api/scheduler/start', 'POST');
    
    if (result && result.success) {
        showNotification('Planificateur démarré', 'success');
    }
}

// Gestion des sites
async function toggleSite(siteId, enabled) {
    const result = await apiCall(`/api/sites/${siteId}`, 'PUT', {enabled});
    
    if (result && result.success) {
        showNotification(result.message, 'success');
    }
}

function showAddSiteForm() {
    document.getElementById('addSiteForm').style.display = 'block';
}

function hideAddSiteForm() {
    document.getElementById('addSiteForm').style.display = 'none';
}

async function addSite() {
    const data = {
        id: document.getElementById('siteId').value,
        name: document.getElementById('siteName').value,
        url: document.getElementById('siteUrl').value,
        timeout: parseInt(document.getElementById('siteTimeout').value),
        enabled: document.getElementById('siteEnabled').checked
    };
    
    if (!data.name || !data.url || !data.id) {
        showNotification('Tous les champs sont requis', 'error');
        return;
    }
    
    const result = await apiCall('/api/sites/new', 'POST', data);
    
    if (result && result.success) {
        showNotification(result.message, 'success');
        setTimeout(() => location.reload(), 1000);
    }
}

// Recherche
async function doSearch() {
    const filters = {
        price_min: parseInt(document.getElementById('priceMin').value) || null,
        price_max: parseInt(document.getElementById('priceMax').value) || null,
        dpe_max: document.getElementById('dpeMax').value,
        location: document.getElementById('location').value,
        status: document.getElementById('status').value
    };
    
    const result = await apiCall('/api/search', 'POST', filters);
    
    const resultsDiv = document.getElementById('results');
    if (result && result.success) {
        if (result.properties && result.properties.length > 0) {
            let html = `<h3>${result.count} résultats trouvés</h3>`;
            html += '<div class="results-list">';
            result.properties.forEach(p => {
                const priceHtml = (p.price || p.price === 0) ? formatPrice(p.price) : 'N/A';
                const surfaceHtml = p.surface ? `${p.surface}m²` : 'N/A';
                const dpe = p.dpe || 'N/A';
                const dpeClass = dpe && typeof dpe === 'string' ? ('dpe-' + dpe.toLowerCase()) : 'dpe-na';
                const sourceBadge = (p.source || 'Unknown').toString().toLowerCase().replace(/\s+/g, '-');
                const location = p.location || 'Non spécifiée';
                const dateHtml = p.posted_date ? new Date(p.posted_date).toLocaleDateString('fr-FR') : 'N/A';

                html += `
                    <div class="result-item card">
                        <strong>${p.title || 'Sans titre'}</strong><br>
                        Prix: ${priceHtml} | 
                        Surface: ${surfaceHtml} | 
                        DPE: <span class="dpe ${dpeClass}">${dpe}</span><br>
                        Zone: ${location} | 
                        Publié: ${dateHtml}<br>
                        Source: <span class="badge badge-${sourceBadge}">${p.source || 'Inconnu'}</span>
                    </div>
                `;
            });
            html += '</div>';
            resultsDiv.innerHTML = html;
        } else {
            resultsDiv.innerHTML = '<p>Aucun résultat trouvé</p>';
        }
    }
}

// Propriétés
async function editProperty(id) {
    const result = await apiCall(`/api/property/${id}`);
    
    if (result && result.success) {
        const prop = result.property;
        const statuses = ['disponible', 'contacté', 'visité', 'rejeté', 'acheté'];
        const currentStatus = statuses.indexOf(prop.status) >= 0 ? prop.status : 'disponible';
        
        const newStatus = prompt('Nouveau statut (' + statuses.join(', ') + '):', currentStatus);
        if (newStatus && statuses.includes(newStatus)) {
            const updateResult = await apiCall(`/api/property/${id}`, 'POST', {status: newStatus});
            if (updateResult && updateResult.success) {
                showNotification('Propriété mise à jour', 'success');
                setTimeout(() => location.reload(), 1000);
            }
        }
    }
}

// Planificateur
async function saveScheduler() {
    const config = {
        interval: parseInt(document.getElementById('interval').value),
        reportTime: document.getElementById('reportTime').value,
        notifications: document.getElementById('enableNotifications').checked
    };
    
    localStorage.setItem('schedulerConfig', JSON.stringify(config));
    showNotification('Configuration enregistrée', 'success');
}

async function updateSchedulerStatus() {
    const result = await apiCall('/api/scheduler/status');
    
    if (result) {
        document.getElementById('runningStatus').textContent = 
            result.running ? 'En cours' : 'Arrêté';
        document.getElementById('lastRun').textContent = result.last_run;
        document.getElementById('nextRun').textContent = result.next_run;
    }
}

async function stopScheduler() {
    if (confirm('Êtes-vous sûr?')) {
        const result = await apiCall('/api/scheduler/stop', 'POST');
        
        if (result && result.success) {
            showNotification(result.message, 'success');
            updateSchedulerStatus();
        }
    }
}

async function runNow() {
    const button = event.target;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scraping...';
    
    const result = await apiCall('/api/scrape', 'POST', {source: 'all'});
    
    button.disabled = false;
    button.innerHTML = '<i class="fas fa-flash"></i> Scraper Maintenant';
    
    if (result && result.success) {
        showNotification(result.message, 'success');
    }
}

// Statistiques
async function loadStats() {
    const result = await apiCall('/api/stats');
    
    if (result) {
        // Mettre à jour les statistiques
        console.log('Stats:', result);
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Mettre à jour le statut du planificateur si sur la page scheduler
    if (document.getElementById('schedulerStatus')) {
        updateSchedulerStatus();
        setInterval(updateSchedulerStatus, 30000); // Toutes les 30s
    }
    
    // Charger les stats si sur le dashboard
    if (document.querySelector('.dashboard')) {
        loadStats();
    }
});

// Styles pour les notifications
const style = document.createElement('style');
style.textContent = `
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    border-radius: 4px;
    background: #2ecc71;
    color: white;
    z-index: 1000;
    transition: opacity 0.3s;
    font-weight: 500;
}

.notification-error {
    background: #e74c3c;
}

.notification-warning {
    background: #f39c12;
}

.notification-info {
    background: #3498db;
}

.result-item {
    margin-bottom: 15px;
    padding: 15px;
}
`;
document.head.appendChild(style);
