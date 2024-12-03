document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    const alertsContainer = document.getElementById('alertsContainer');
    const estadoSelect = document.getElementById('estado');
    const tipoSelect = document.getElementById('tipo');

    // Llenar los selects
    function fillSelects() {
        Object.entries(estados).forEach(([value, text]) => {
            const option = new Option(text, value);
            estadoSelect.add(option);
        });

        Object.entries(tipos).forEach(([value, text]) => {
            const option = new Option(text, value);
            tipoSelect.add(option);
        });
    }

    // Formatear fecha
    function formatDate(dateString) {
        const fecha = new Date(dateString);
        return fecha.toLocaleString('es-ES', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function renderAlertas(alertas) {
        alertsContainer.innerHTML = '';
        
        if (alertas.length === 0) {
            alertsContainer.innerHTML = '<p class="no-alerts">No hay alertas que mostrar.</p>';
            return;
        }

        alertas.forEach(alerta => {
            const card = document.createElement('div');
            card.className = `alert-card ${alerta.estado}`;
            
            const actions = alerta.estado === 'en_proceso' 
                ? `<button class="btn btn-success resolver-btn" data-id="${alerta.id}">Resolver</button>`
                : `<button class="btn btn-primary atender-btn" data-id="${alerta.id}" ${alerta.estado === 'resuelta' ? 'disabled' : ''}>
                     Atender
                   </button>`;

            card.innerHTML = `
                <div class="alert-header">
                    <span class="alert-title">${tipos[alerta.tipo]}</span>
                    <span class="alert-date">${formatDate(alerta.fecha_creacion)}</span>
                </div>
                <div class="alert-description">${alerta.descripcion}</div>
                <div class="alert-footer">
                    <span>Módulo: ${alerta.modulo ? alerta.modulo.nombre : 'No asignado'}</span>
                    <span>Estado: ${estados[alerta.estado]}</span>
                </div>
                <div class="alert-actions">
                    ${actions}
                    <button class="btn btn-secondary detalles-btn" data-id="${alerta.id}">
                        Detalles
                    </button>
                </div>
            `;
            alertsContainer.appendChild(card);
        });

        document.querySelectorAll('.atender-btn').forEach(btn => {
            btn.addEventListener('click', atenderAlerta);
        });
        
        document.querySelectorAll('.resolver-btn').forEach(btn => {
            btn.addEventListener('click', resolverAlerta);
        });
        
        document.querySelectorAll('.detalles-btn').forEach(btn => {
            btn.addEventListener('click', verDetalles);
        });
    }

    // Filtrar alertas
    function filtrarAlertas(e) {
        if (e) e.preventDefault();
        
        const estadoFiltro = estadoSelect.value;
        const tipoFiltro = tipoSelect.value;

        const alertasFiltradas = alertasIniciales.filter(alerta => {
            const cumpleEstado = !estadoFiltro || alerta.estado === estadoFiltro;
            const cumpleTipo = !tipoFiltro || alerta.tipo === tipoFiltro;
            return cumpleEstado && cumpleTipo;
        });

        renderAlertas(alertasFiltradas);
    }

    function atenderAlerta(event) {
        const alertaId = event.target.dataset.id;
        fetch(`/atender-alerta/${alertaId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const alerta = alertasIniciales.find(a => a.id.toString() === alertaId);
                if (alerta) {
                    alerta.estado = 'en_proceso';
                    filtrarAlertas();
                }
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al atender la alerta');
        });
    }

    function resolverAlerta(event) {
        const alertaId = event.target.dataset.id;
        fetch(`/resolver-alerta/${alertaId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const alerta = alertasIniciales.find(a => a.id.toString() === alertaId);
                if (alerta) {
                    alerta.estado = 'resuelta';
                    filtrarAlertas();
                }
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al resolver la alerta');
        });
    }

    function verDetalles(event) {
        const alertaId = event.target.dataset.id;
        const alerta = alertasIniciales.find(a => a.id.toString() === alertaId);
        
        if (!alerta) return;

        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Detalles de la Alerta</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <p><strong>Tipo:</strong> ${tipos[alerta.tipo]}</p>
                    <p><strong>Estado:</strong> ${estados[alerta.estado]}</p>
                    <p><strong>Módulo:</strong> ${alerta.modulo ? alerta.modulo.nombre : 'No asignado'}</p>
                    <p><strong>Fecha:</strong> ${formatDate(alerta.fecha_creacion)}</p>
                    <p><strong>Descripción:</strong> ${alerta.descripcion}</p>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        const closeBtn = modal.querySelector('.close-modal');
        closeBtn.addEventListener('click', () => {
            modal.remove();
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

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

    fillSelects();
    renderAlertas(alertasIniciales);
    filterForm.addEventListener('submit', filtrarAlertas);
});