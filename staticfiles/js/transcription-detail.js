/**
 * Transcription Detail - Copy Functionality
 * Handles copying transcription text to clipboard with fallback support
 */

/**
 * Copy transcription to clipboard
 */
function copyTranscription() {
    const text = document.getElementById('full-transcription').textContent;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            // Show success notification
            const toast = document.createElement('div');
            toast.className = 'alert alert-success alert-dismissible fade show';
            toast.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
            toast.innerHTML = `
                <i class="fas fa-check me-2"></i>Transcripción copiada al portapapeles
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                if (toast && toast.parentNode) {
                    toast.remove();
                }
            }, 3000);
        }).catch(() => {
            showCustomAlert('Error al copiar. Selecciona el texto manualmente.', 'error', 3000);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showCustomAlert('Transcripción copiada al portapapeles', 'success', 2500);
    }
}
