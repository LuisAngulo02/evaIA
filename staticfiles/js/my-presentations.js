/**
 * EvalExpo AI - JavaScript para Mis Presentaciones
 * Manejo de borrado y actualización de progreso de presentaciones
 */

// Confirmación de borrado de presentación
function confirmDelete(presentationId, title) {
    document.getElementById('presentationTitle').textContent = title;
    document.getElementById('deleteForm').action = `/presentations/presentation/${presentationId}/delete/`;
    
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

// Función para actualizar progreso de presentación
function updateProgress(presentationId) {
    fetch(`/presentations/api/presentation-progress/${presentationId}/`)
        .then(response => response.json())
        .then(data => {
            const progressBar = document.getElementById(`progress-bar-${presentationId}`);
            const progressText = document.getElementById(`progress-text-${presentationId}`);
            const progressStep = document.getElementById(`progress-step-${presentationId}`);
            
            if (progressBar && data.progress !== undefined) {
                progressBar.style.width = data.progress + '%';
                progressBar.setAttribute('aria-valuenow', data.progress);
                
                if (progressText) {
                    progressText.textContent = data.progress + '%';
                }
                
                if (progressStep && data.step) {
                    progressStep.innerHTML = `<i class="fas fa-cog fa-spin me-1"></i>${data.step}`;
                }
                
                // Si completó (100%), recargar página después de 2 segundos
                if (data.progress >= 100 || data.status === 'ANALYZED') {
                    progressBar.classList.remove('progress-bar-animated');
                    progressBar.classList.add('bg-success');
                    if (progressStep) {
                        progressStep.innerHTML = `<i class="fas fa-check-circle me-1"></i>Completado - Recargando...`;
                    }
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                } else if (data.status === 'FAILED') {
                    progressBar.classList.remove('progress-bar-animated', 'bg-info');
                    progressBar.classList.add('bg-danger');
                    if (progressStep) {
                        progressStep.innerHTML = `<i class="fas fa-times-circle me-1"></i>Error en análisis`;
                    }
                }
            }
        })
        .catch(error => {
            console.error('Error al obtener progreso:', error);
        });
}

// Inicializar monitoreo de presentaciones en procesamiento
function initProgressMonitoring(processingPresentations) {
    if (processingPresentations.length > 0) {
        processingPresentations.forEach(presentationId => {
            // Actualizar inmediatamente
            updateProgress(presentationId);
            
            // Continuar actualizando cada 3 segundos
            const intervalId = setInterval(() => {
                updateProgress(presentationId);
            }, 3000);
            
            // Guardar ID del intervalo para poder detenerlo
            window[`progress_interval_${presentationId}`] = intervalId;
        });
    }
}

// Export functions
window.confirmDelete = confirmDelete;
window.updateProgress = updateProgress;
window.initProgressMonitoring = initProgressMonitoring;
