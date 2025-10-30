/**
 * Edit Participant Grade Logic
 * Template: edit_participant_grade.html
 * Description: Handles grade reset functionality
 */

/**
 * Reset participant grade to AI-generated grade
 * @param {string} resetUrl - URL endpoint to reset the grade
 * @param {string} csrfToken - CSRF token for POST request
 */
function resetGrade(resetUrl, csrfToken) {
    if (confirm('¿Estás seguro de que quieres restaurar la calificación de IA? Se perderán los cambios manuales.')) {
        fetch(resetUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                showCustomAlert('Error: ' + data.error, 'error', 4000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showCustomAlert('Ocurrió un error al restaurar la calificación.', 'error', 4000);
        });
    }
}
