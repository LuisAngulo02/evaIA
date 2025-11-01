/* ============================================================
   TEACHER REPORTS JAVASCRIPT
   Funciones para exportación y animaciones de reportes
   ============================================================ */

/**
 * Exporta datos del reporte en el formato especificado
 * @param {string} format - Formato de exportación ('pdf', 'excel', etc.)
 */
function exportData(format) {
    if (format === 'pdf') {
        console.log('Exportando reporte completo a PDF...');
        showExportMessage('Generando reporte PDF...', 'success');
        window.location.href = "{% url 'reports:export_grades_pdf' %}";
    }
}

/**
 * Exporta los datos de un curso específico
 * @param {number} courseId - ID del curso a exportar
 * @param {string} format - Formato de exportación ('pdf', 'excel', etc.)
 */
function exportCourse(courseId, format) {
    console.log(`Exportando curso ${courseId} en formato ${format}...`);
    showExportMessage(`Generando archivo ${format.toUpperCase()}...`, 'info');
    window.location.href = `/reports/export/course/${courseId}/?format=${format}`;
}

/**
 * Muestra un mensaje temporal de notificación de exportación
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de alerta ('success', 'info', 'warning', 'danger')
 */
function showExportMessage(message, type) {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show export-notification`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-download me-2"></i>
            <span>${message}</span>
            <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Agregar al body
    document.body.appendChild(notification);
    
    // Auto-remover después de 3 segundos
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

/**
 * Animaciones de entrada cuando la página carga
 * Anima las tarjetas con efecto de fade-in escalonado
 */
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.stat-card, .course-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});
