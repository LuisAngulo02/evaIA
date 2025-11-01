/**
 * EvalExpo AI - Utilidades Comunes
 * Funciones reutilizables para tabs, AJAX y manejo de UI
 */

/**
 * Cambia entre tabs
 * @param {string} tabId - ID del tab a activar
 */
function switchTab(tabId) {
    // Remover clase active de todos los tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Activar tab seleccionado
    const selectedTab = document.getElementById(tabId);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Activar botón correspondiente
    const selectedBtn = document.querySelector(`[data-tab="${tabId}"]`);
    if (selectedBtn) {
        selectedBtn.classList.add('active');
    }

    // Si se activa el tab de grabación, iniciar cámara
    if (tabId === 'record-tab') {
        // La cámara se inicializa con el código de recording.js
        if (typeof initCamera === 'function') {
            setTimeout(() => initCamera(), 300);
        }
    }
}

/**
 * Carga los detalles de una asignación via AJAX
 * @param {string|number} assignmentId - ID de la asignación
 * @param {string} targetElement - ID del elemento donde mostrar los detalles
 */
function loadAssignmentDetails(assignmentId, targetElement = 'assignment-info-upload') {
    if (!assignmentId) {
        hideAssignmentDetails(targetElement);
        return;
    }

    fetch(`/presentations/api/assignment-details/?assignment_id=${assignmentId}`)
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                showAssignmentDetails(data, targetElement);
            } else {
                console.error('Error cargando detalles:', data.error);
                hideAssignmentDetails(targetElement);
            }
        })
        .catch(error => {
            console.error('Error en la petición:', error);
            hideAssignmentDetails(targetElement);
        });
}

/**
 * Muestra los detalles de una asignación en el DOM
 * @param {Object} data - Datos de la asignación
 * @param {string} targetElement - ID del elemento destino
 */
function showAssignmentDetails(data, targetElement) {
    const detailsContainer = targetElement === 'assignment-info-upload' 
        ? document.getElementById('assignment-details-upload')
        : document.getElementById('assignment-details-recording');
    
    const infoElement = document.getElementById(targetElement);
    
    if (!infoElement) return;

    const html = `
        <div class="row">
            <div class="col-md-6">
                <p><strong><i class="fas fa-book me-2"></i>Curso:</strong> ${data.course}</p>
                <p><strong><i class="fas fa-tag me-2"></i>Tipo:</strong> ${data.type}</p>
                <p><strong><i class="fas fa-clock me-2"></i>Duración máxima:</strong> ${data.max_duration} min</p>
            </div>
            <div class="col-md-6">
                <p><strong><i class="fas fa-calendar me-2"></i>Fecha límite:</strong> ${data.due_date}</p>
                <p><strong><i class="fas fa-star me-2"></i>Puntaje máximo:</strong> ${data.max_score} puntos</p>
                <p><strong><i class="fas fa-user-tie me-2"></i>Docente:</strong> ${data.teacher}</p>
            </div>
        </div>
        <div class="mt-3 pt-3 border-top">
            <h6 class="mb-2">
                <i class="fas fa-list-ul me-2 text-primary"></i>
                <strong>Instrucciones:</strong>
            </h6>
            <div class="alert alert-primary" style="background-color: rgba(99, 102, 241, 0.1); border-color: rgba(99, 102, 241, 0.2);">
                <i class="fas fa-info-circle me-2"></i>
                ${data.instructions ? data.instructions.replace(/\n/g, '<br>') : 'No hay instrucciones específicas para esta asignación.'}
            </div>
        </div>
    `;
    
    infoElement.innerHTML = html;
    
    if (detailsContainer) {
        detailsContainer.style.display = 'block';
    }
}

/**
 * Oculta los detalles de asignación
 * @param {string} targetElement - ID del elemento destino
 */
function hideAssignmentDetails(targetElement) {
    const detailsContainer = targetElement === 'assignment-info-upload' 
        ? document.getElementById('assignment-details-upload')
        : document.getElementById('assignment-details-recording');
    
    if (detailsContainer) {
        detailsContainer.style.display = 'none';
    }
}

/**
 * Sincroniza el valor entre dos selectores
 * @param {string} sourceId - ID del selector origen
 * @param {string} targetId - ID del selector destino
 */
function syncSelectors(sourceId, targetId) {
    const source = document.getElementById(sourceId);
    const target = document.getElementById(targetId);
    
    if (source && target) {
        target.value = source.value;
    }
}

/**
 * Muestra un mensaje de carga
 * @param {string} message - Mensaje a mostrar
 */
function showLoading(message = 'Cargando...') {
    // Implementación simple - puede mejorarse con un modal o overlay
    console.log(message);
}

/**
 * Oculta el mensaje de carga
 */
function hideLoading() {
    console.log('Carga completada');
}

// Exportar funciones globalmente
window.switchTab = switchTab;
window.loadAssignmentDetails = loadAssignmentDetails;
window.syncSelectors = syncSelectors;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
