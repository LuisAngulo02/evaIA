/* ============================================================
   MANAGE STUDENTS JAVASCRIPT
   Funciones para búsqueda y gestión de estudiantes
   ============================================================ */

// Variables globales
let searchTimeout;
const searchInput = document.getElementById('searchInput');
const studentsList = document.getElementById('availableStudentsList');
const loadingIndicator = document.getElementById('loadingIndicator');
const courseId = document.querySelector('[data-course-id]')?.dataset.courseId;

/**
 * Inicialización al cargar el DOM
 */
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar mensaje inicial (sin cargar estudiantes)
    if (studentsList) {
        studentsList.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-search text-muted mb-3" style="font-size: 3rem; opacity: 0.3;"></i>
                <p class="text-muted">Escribe para buscar estudiantes</p>
                <small class="text-muted">Busca por nombre, correo o usuario</small>
            </div>
        `;
    }
    
    // Configurar búsqueda con debounce
    if (searchInput) {
        searchInput.addEventListener('input', handleSearchInput);
    }
});

/**
 * Maneja el input de búsqueda con debounce
 */
function handleSearchInput() {
    clearTimeout(searchTimeout);
    const query = this.value.trim();
    
    // Si el campo está vacío, mostrar mensaje inicial
    if (query === '') {
        studentsList.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-search text-muted mb-3" style="font-size: 3rem; opacity: 0.3;"></i>
                <p class="text-muted">Escribe para buscar estudiantes</p>
                <small class="text-muted">Busca por nombre, correo o usuario</small>
            </div>
        `;
        return;
    }
    
    // Mostrar loading solo si hay texto
    loadingIndicator.style.display = 'block';
    studentsList.style.display = 'none';
    
    searchTimeout = setTimeout(() => {
        loadAvailableStudents(query);
    }, 300); // 300ms de debounce
}

/**
 * Carga estudiantes disponibles mediante AJAX
 * @param {string} query - Término de búsqueda
 */
function loadAvailableStudents(query) {
    const url = `/presentations/courses/${courseId}/students/api/?search=${encodeURIComponent(query)}`;
    
    fetch(url, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        loadingIndicator.style.display = 'none';
        studentsList.style.display = 'block';
        
        if (data.students && data.students.length > 0) {
            renderStudentsList(data.students);
        } else {
            renderEmptyState(query);
        }
    })
    .catch(error => {
        console.error('Error al buscar estudiantes:', error);
        renderErrorState();
    });
}

/**
 * Renderiza la lista de estudiantes disponibles
 * @param {Array} students - Array de estudiantes
 */
function renderStudentsList(students) {
    studentsList.innerHTML = students.map(student => `
        <div class="available-student-item border-bottom py-2">
            <div class="d-flex justify-content-between align-items-center">
                <div class="flex-grow-1">
                    <div class="fw-semibold">
                        ${student.full_name || student.username}
                    </div>
                    <small class="text-muted d-block">
                        <i class="fas fa-user me-1"></i>${student.username}
                    </small>
                    <small class="text-muted d-block">
                        <i class="fas fa-envelope me-1"></i>${student.email}
                    </small>
                </div>
                <form method="POST" style="display: inline;" onsubmit="handleEnrollSubmit(event, ${student.id}, '${student.full_name || student.username}')">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
                    <input type="hidden" name="action" value="add_student">
                    <input type="hidden" name="student_id" value="${student.id}">
                    <button type="submit" class="btn btn-sm btn-success" 
                            title="Matricular estudiante">
                        <i class="fas fa-plus"></i>
                    </button>
                </form>
            </div>
        </div>
    `).join('');
}

/**
 * Renderiza estado vacío cuando no hay resultados
 * @param {string} query - Término de búsqueda
 */
function renderEmptyState(query) {
    if (query) {
        studentsList.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-search text-muted mb-3" style="font-size: 3rem; opacity: 0.3;"></i>
                <p class="text-muted">No se encontraron estudiantes con "${query}"</p>
                <small class="text-muted">Intenta buscar por nombre, correo o usuario</small>
            </div>
        `;
    } else {
        studentsList.innerHTML = `
            <div class="text-center py-4">
                <i class="fas fa-check-circle text-success mb-3" style="font-size: 3rem; opacity: 0.3;"></i>
                <p class="text-muted">Todos los estudiantes ya están matriculados</p>
            </div>
        `;
    }
}

/**
 * Renderiza estado de error
 */
function renderErrorState() {
    loadingIndicator.style.display = 'none';
    studentsList.style.display = 'block';
    studentsList.innerHTML = `
        <div class="text-center py-4">
            <i class="fas fa-exclamation-triangle text-warning mb-3" style="font-size: 3rem; opacity: 0.3;"></i>
            <p class="text-muted">Error al cargar estudiantes</p>
            <button onclick="loadAvailableStudents('')" class="btn btn-sm btn-outline-primary mt-2">
                <i class="fas fa-sync-alt me-1"></i>Reintentar
            </button>
        </div>
    `;
}

/**
 * Obtiene el valor de una cookie
 * @param {string} name - Nombre de la cookie
 * @returns {string|null} Valor de la cookie
 */
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

/**
 * Maneja el envío del formulario de matriculación
 * @param {Event} event - Evento del formulario
 * @param {number} studentId - ID del estudiante
 * @param {string} studentName - Nombre del estudiante
 */
async function handleEnrollSubmit(event, studentId, studentName) {
    event.preventDefault();
    
    // Usar confirmación personalizada
    const confirmed = await customConfirm(
        `¿Estás seguro de matricular a <strong>${studentName}</strong> en este curso?`,
        'Sí, matricular',
        'Cancelar'
    );
    
    if (!confirmed) {
        return;
    }
    
    const formData = new FormData(event.target);
    
    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Mostrar mensaje de éxito con alerta personalizada
            showCustomAlert(data.message, 'success');
            
            // Recargar solo la página para actualizar la lista de matriculados
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showCustomAlert(data.message || 'Error al matricular estudiante', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showCustomAlert('Error al procesar la solicitud', 'error');
    });
}

/**
 * Maneja el envío del formulario de desmatriculación
 * @param {Event} event - Evento del formulario
 * @param {string} studentName - Nombre del estudiante
 * @returns {boolean} - False para prevenir el submit normal
 */
async function handleUnenrollSubmit(event, studentName) {
    event.preventDefault();
    
    // Usar confirmación personalizada
    const confirmed = await customConfirm(
        `¿Estás seguro de desmatricular a <strong>${studentName}</strong> de este curso?<br><small class="text-muted">Esta acción no se puede deshacer.</small>`,
        'Sí, desmatricular',
        'Cancelar'
    );
    
    if (confirmed) {
        // Mostrar alerta de procesamiento
        showCustomAlert('Desmatriculando estudiante...', 'info', 2000);
        // Enviar el formulario
        event.target.submit();
    }
    
    return false;
}

/**
 * Muestra notificación toast temporal
 * @param {string} type - Tipo de notificación ('success' o 'error')
 * @param {string} message - Mensaje a mostrar
 */
function showToast(type, message) {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'success' ? 'success' : 'danger'} position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
        ${message}
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}
