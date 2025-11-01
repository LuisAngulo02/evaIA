/**
 * Presentation Deletion Confirmation Logic
 * Template: confirm_delete.html
 * Description: Handles presentation deletion confirmation and safety features
 */

/**
 * Shows final confirmation dialog before deletion
 * @returns {boolean} True if user confirms deletion
 */
function confirmFinalDelete() {
    return confirm(
        '¿Estás completamente seguro de que deseas eliminar esta presentación?\n\n' +
        'Esta acción NO SE PUEDE DESHACER y se eliminará:\n' +
        '- El archivo de video\n' +
        '- Todos los análisis de IA\n' +
        '- La calificación (si existe)\n' +
        '- Todo el historial asociado\n\n' +
        'Escribe "ELIMINAR" para confirmar:'
    );
}

/**
 * Auto-focus on cancel button for safety
 */
function initDeleteConfirmation() {
    const cancelBtn = document.querySelector('.btn-outline-secondary');
    if (cancelBtn) {
        cancelBtn.focus();
    }
}

/**
 * Setup keyboard shortcuts for deletion confirmation
 * @param {string} cancelUrl - URL to redirect when ESC is pressed
 */
function setupDeleteKeyboardShortcuts(cancelUrl) {
    document.addEventListener('keydown', function(e) {
        // ESC to cancel
        if (e.key === 'Escape' && cancelUrl) {
            window.location.href = cancelUrl;
        }
        
        // Prevent accidental Enter submission
        if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') {
            e.preventDefault();
        }
    });
}
