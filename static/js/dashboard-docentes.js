/* ============================================================
   DASHBOARD DOCENTES JAVASCRIPT
   Funciones para el dashboard de docentes
   ============================================================ */

/**
 * Muestra notificación temporal de exportación
 * @param {string} format - Formato de exportación ('Excel', 'PDF')
 */
function showExportNotification(format) {
    const notification = document.createElement('div');
    notification.className = 'alert alert-info alert-dismissible fade show export-notification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease-out;
    `;
    
    notification.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-download me-2"></i>
            <span>Generando archivo ${format}...</span>
            <button type="button" class="btn-close ms-auto" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.remove();
        }
    }, 4000);
}

// ===== EVENT LISTENERS =====

document.addEventListener('DOMContentLoaded', function() {
    // Enlaces de exportación Excel y PDF
    document.querySelectorAll('a[href*="export_grades"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const format = this.href.includes('excel') ? 'Excel' : 'PDF';
            showExportNotification(format);
        });
    });
    
    // Animar las barras de progreso con efecto shimmer
    const shimmerBars = document.querySelectorAll('.shimmer-bar');
    
    shimmerBars.forEach(function(bar, index) {
        const percentage = bar.getAttribute('data-percentage');
        
        // Animar el ancho con delay escalonado
        setTimeout(function() {
            bar.style.width = percentage + '%';
        }, 200 + (index * 300));
    });
});
