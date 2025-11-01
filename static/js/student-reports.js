/**
 * Student Reports Logic
 * Template: student_reports.html
 * Description: Handles student grade export and UI animations
 */

/**
 * Export student data to specified format
 * @param {string} format - Export format (currently supports 'pdf')
 * @param {string} exportUrl - URL to trigger the export
 */
function exportStudentData(format, exportUrl) {
    if (format === 'pdf') {
        console.log('Exportando mis calificaciones a PDF...');
        showExportMessage('Generando mi reporte PDF...', 'success');
        window.location.href = exportUrl + '?format=pdf';
    }
}

/**
 * Show export notification message
 * @param {string} message - Message to display
 * @param {string} type - Bootstrap alert type (success, info, warning, danger)
 */
function showExportMessage(message, type) {
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
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification && notification.parentNode) {
            notification.remove();
        }
    }, 3000);
}

/**
 * Animate cards on page load with staggered entrance
 */
function animateCardsEntrance() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Initialize animations on page load
document.addEventListener('DOMContentLoaded', animateCardsEntrance);
