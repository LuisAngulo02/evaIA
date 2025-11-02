/**
 * Bulk Grade Logic
 * Template: bulk_grade.html
 * Description: Handles bulk grading with auto-save and validation
 */

/**
 * Initialize bulk grading form with auto-save functionality
 */
function initBulkGrading() {
    const form = document.getElementById('bulkGradingForm');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, textarea');

    // Load saved values from localStorage
    inputs.forEach(input => {
        const saved = localStorage.getItem(`grade_${input.name}`);
        if (saved && input.value === input.defaultValue) {
            input.value = saved;
        }
        
        // Save on change
        input.addEventListener('change', () => {
            localStorage.setItem(`grade_${input.name}`, input.value);
        });
    });

    // Clear localStorage on submit
    form.addEventListener('submit', () => {
        inputs.forEach(input => {
            localStorage.removeItem(`grade_${input.name}`);
        });
    });

    // Validate grades before submit
    form.addEventListener('submit', function(e) {
        const gradeInputs = form.querySelectorAll('[name^="grade_"]');
        let hasError = false;
        
        gradeInputs.forEach(input => {
            const value = parseFloat(input.value);
            if (value < 0 || value > 20) {
                hasError = true;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        if (hasError) {
            e.preventDefault();
            showCustomAlert('Por favor, verifica que todas las calificaciones estén entre 0 y 20.', 'warning', 4000);
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initBulkGrading);
