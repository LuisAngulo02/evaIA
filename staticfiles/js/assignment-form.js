/**
 * Assignment Form - AI Instructions Improvement
 * Handles AI-powered instruction enhancement with context awareness
 */

/**
 * Improve assignment instructions using AI
 * @async
 */
async function improveInstructions() {
    const instructionsField = document.getElementById(document.querySelector('[name="instructions"]').id);
    const currentInstructions = instructionsField.value.trim();
    
    // Validations
    if (!currentInstructions) {
        showCustomAlert('Por favor escribe algunas instrucciones básicas primero', 'warning', 3000);
        instructionsField.focus();
        return;
    }
    
    if (currentInstructions.length < 20) {
        showCustomAlert('Las instrucciones son muy cortas. Escribe al menos una idea básica (mínimo 20 caracteres)', 'warning', 3500);
        return;
    }
    
    // Get additional context
    const titleField = document.querySelector('[name="title"]');
    const descriptionField = document.querySelector('[name="description"]');
    const assignmentTypeField = document.querySelector('[name="assignment_type"]');
    const durationField = document.querySelector('[name="max_duration"]');
    
    const title = titleField ? titleField.value : '';
    const description = descriptionField ? descriptionField.value : '';
    const assignmentType = assignmentTypeField ? assignmentTypeField.selectedOptions[0]?.text : '';
    const duration = durationField ? durationField.value : '';
    
    // UI feedback elements
    const btn = document.getElementById('improveInstructionsBtn');
    const loadingIndicator = document.getElementById('aiLoadingIndicator');
    const successIndicator = document.getElementById('aiSuccessIndicator');
    const errorIndicator = document.getElementById('aiErrorIndicator');
    
    // Reset indicators
    if (successIndicator) successIndicator.style.display = 'none';
    if (errorIndicator) errorIndicator.style.display = 'none';
    
    // Disable button and show loading
    btn.disabled = true;
    btn.classList.add('loading');
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    
    try {
        // Get improve URL from the script tag
        const scriptTag = document.querySelector('script[data-improve-url]');
        const improveUrl = scriptTag ? scriptTag.dataset.improveUrl : '/presentations/api/improve-instructions-ai/';
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        const response = await fetch(improveUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                instructions: currentInstructions,
                context: {
                    title: title,
                    description: description,
                    assignment_type: assignmentType,
                    max_duration: duration
                }
            })
        });
        
        // Check if response is ok before parsing JSON
        if (!response.ok) {
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Error del servidor: ${response.status}`);
            } else {
                // Response is HTML (probably an error page)
                throw new Error(`Error del servidor: ${response.status}. Verifica que tengas permisos de profesor.`);
            }
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Update field with improved instructions
            instructionsField.value = data.improved_instructions;
            
            // Show success alert with custom alert system
            showCustomAlert('¡Instrucciones mejoradas con IA exitosamente!', 'success', 4000);
            
            // Auto scroll to field
            instructionsField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            throw new Error(data.error || 'Error desconocido');
        }
        
    } catch (error) {
        console.error('Error mejorando instrucciones:', error);
        
        // Show error with custom alert system
        showCustomAlert(
            error.message || 'No se pudo conectar con el servicio de IA. Intenta de nuevo.',
            'error',
            5000
        );
    } finally {
        // Re-enable button
        btn.disabled = false;
        btn.classList.remove('loading');
        if (loadingIndicator) loadingIndicator.style.display = 'none';
    }
}

/**
 * Initialize keyboard shortcuts
 */
document.addEventListener('DOMContentLoaded', function() {
    // Keyboard shortcut: Ctrl+Alt+I
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.altKey && e.key === 'i') {
            e.preventDefault();
            improveInstructions();
        }
    });
});
